import requests
import re
import json
import pandas as pd
from pandas.io.json import json_normalize
import time
from requests.adapters import HTTPAdapter
from datetime import datetime, timedelta, timezone

from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 35116)

city_level = client['ncov_illness']["city_level"]
province_level = client['ncov_illness']["province_level"]
country_level = client['ncov_illness']["country_level"]





def get_html():

    i = 0
    # print(time.strftime('%Y-%m-%d %H:%M:%S'))

    while i < 6:
        try:
            r = requests.get('https://3g.dxy.cn/newh5/view/pneumonia?from=timeline&isappinstalled=0',timeout=60)
            r.encoding = "utf-8"
            content = r.text
            return content
        except requests.exceptions.RequestException as e:
            i += 1
            print(e)
    # print(time.strftime('%Y-%m-%d %H:%M:%S'))
    # with open("sta")


def get_soup(html):

    soup = BeautifulSoup(html,"lxml")

    return soup

def parse_date(soup):

    p = soup.find("p",{"class":"mapTitle___2QtRg"})
    date_str = p.text.strip("截至 ").strip("（北京时间）数据统计").strip("（北京时间）全国数据统计")
# 截至 2020-01-25 17:32（北京时间）数据统计
# 截至 2020-01-28 12:15（北京时间）全国数据统计


    date_ = datetime.strptime(date_str,"%Y-%m-%d %H:%M")
    return date_



def get_data_str(soup):

# 匹配数据内容

    script1 = soup.find("script",{"id":"getAreaStat"}).text
    script2 = soup.find("script",{"id":"getListByCountryTypeService1"}).text
    script3 = soup.find("script",{"id":"getListByCountryTypeService2"}).text

    with open("test.html","w",encoding="utf-8") as f:
    #     # f.write(script1)
        f.write(script2)
        
# 缩小数据内容范围
    data_body1 = script1.strip(r'''}catch(e){}''').strip(r'''try { window.getAreaStat =''')
    data_body2 = script2.strip(r'''}catch(e){}''').strip(r'''try { window.getListByCountryTypeService1 = ''')
    data_body3 = script3.strip(r'''}catch(e){}''').strip(r'''try { window.getListByCountryTypeService2 = ''')

    with open("test.html","w",encoding="utf-8") as f:
        # f.write(script1)
        f.write(data_body2)

#  筛选所需要的数据
    # data_str = data_body.split(r'''}catch(e){}</script><script id="getListByCountryTypeService1">try { window.getListByCountryTypeService1 =''')

    return json.loads(data_body1),json.loads(data_body2),json.loads(data_body3)

def parse_data1(data):


    dataset = json_normalize(data,"cities",["provinceName","provinceShortName","confirmedCount","suspectedCount","curedCount","deadCount","comment"],record_prefix='city.')
    return dataset

def parse_data2(data):

    # data = json.loads(data_str)
    dataset = json_normalize(data)

    return dataset


def save_data_to_csv(dataset,fileName):

    dataset.to_csv(fileName,encoding = "utf-8")

def save_to_db(data_body,db,crawler_time,until_now):

    data = []
    for item in data_body:
        item["crawler_time"] = crawler_time
        item["until_now"] = until_now
        data.append(item)
        db.insert_one(item)   
    return data

if __name__ == '__main__':
    
    while True:

# 从电脑获取抓取数据的时间
        utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
        # print(utc_dt)
        cn_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
        crawler_time = cn_dt.isoformat()
        print(crawler_time)
        fileName_date =  crawler_time[:13]


        html = get_html()
# 保存数据
        with open("static/raw_html/%s.html"%fileName_date, "w",encoding = "utf-8") as f:
            f.write(html)

        soup = get_soup(html)

# 从网页获得数据更新时间
        try:
            date_ = parse_date(soup)
            until_now = date_.isoformat()
        except Exception as e:
            print(e)
            until_now = crawler_time
        print(until_now)
        # fileName_date = until_now[:13]

        data_body1,data_body2,data_body3 = get_data_str(soup)

# 添加事件信息
# 这里的长度是不一样的，这个数据完全不能使用？？？应该是添加完国家的数据之后的数据都是不能用的，主要是确实很多数据
        
        data1 = save_to_db(data_body1,city_level,crawler_time,until_now)
        data2 = save_to_db(data_body2,province_level,crawler_time,until_now)
        data3 = save_to_db(data_body3,country_level,crawler_time,until_now)

        dataset1 = parse_data1(data1)
        dataset2 = parse_data2(data2)
        dataset3 = parse_data2(data3)

        save_data_to_csv(dataset1,"static/data/city_level_%s.csv"%fileName_date)
        save_data_to_csv(dataset2,"static/data/province_level_%s.csv"%fileName_date)
        save_data_to_csv(dataset3,"static/data/country_level_%s.csv"%fileName_date)

        time.sleep(3600)

# TODO: 增加时间控制
# 1. 每个小时搜集一次数据
# 2. 在数据的时间集中控制
# 3. 数据库可以使用sqlite
    

