import geopandas as gpd
import os
import json 
from shapely.geometry import Point
from geopy.geocoders import Baidu
import time
import matplotlib.pyplot as plt
import requests
import pandas as pd
from datetime import datetime, timedelta

GEOLOCATOR = Baidu(
            api_key='',#自己修改
           
            timeout=60
        )


def get_data_from_url(url):

    response = requests.get(url)
    data = json.loads(response.text)
    data = pd.DataFrame(data)

    return data

def load_geo_code_dict():

    with open("static/geo_map.json","r",encoding = "utf-8") as f:
        mm = f.read()
    geo_code_dict = json.loads(mm)

    return geo_code_dict

def update_geo_code_dict(geo_code_dict):

    with open("static/geo_map.json","w",encoding = "utf-8") as f:
        f.write(json.dumps(geo_code_dict,ensure_ascii=False))

def geo_coding(data,geo_code_dict,geolocator):
    # 如果有没有在geo_code_dict的要使用编码器编码并更新dict

    for k,v in data.iterrows():
        
        name = v["city.cityName"]

        if name in geo_code_dict:
            continue

        print(name)
        name_ = name
        if name == "湘西自治州":
            name_ = "湘西土家族苗族自治州"
        if name == "伊犁州":
            name_ = "伊犁哈萨克自治州"
        
        locator = geolocator.geocode(name_,timeout=60)
        geo_code_dict[name] = (locator.longitude,locator.latitude)
        time.sleep(2)

    update_geo_code_dict(geo_code_dict)

def get_point_geo(xy):   
    p = Point((*xy))
    return p

def tansferxy2geopandas(data,geo_code_dict):

    data.loc[:,"geometry"] = data['city.cityName'].map(lambda x: get_point_geo(geo_code_dict[x]))

    geo_data = gpd.GeoDataFrame(data, geometry=data["geometry"].values)

    

    return geo_data

def load_base_map():

    china_map = gpd.read_file("static/china-geojson/china.json")

    path = "static/china-geojson/geometryProvince/"
    provinces_list = []
    for fileName in os.listdir(path):
        province_geo = gpd.read_file(path + fileName)
        provinces_list.append(province_geo)
    city_map = pd.concat(provinces_list,sort=False)
        
    return china_map,city_map

def city_sjoin(city_map,data):
    joined_data = gpd.sjoin(city_map,data)
    return joined_data

def make_ch_map(basemap,joined_data,fileName):

    fig, ax = plt.subplots(1, 1,figsize=(16,9))
# divider = make_axes_locatable(ax)
# cax = divider.append_axes("right", size="5%", pad=0.1)

# cities.plot(ax=ax,color = "white",edgecolor='black',alpha=0.5);
    basemap.plot(ax=ax,color = "white",edgecolor='black',alpha=0.7);
    joined_data[joined_data["city.confirmedCount"].map(lambda x: 0<x<10 )].plot( ax=ax,color = "#f08e7e");
    joined_data[joined_data["city.confirmedCount"].map(lambda x: x >=10 and x<100 )].plot( ax=ax,color = "#e04b49");
    joined_data[joined_data["city.confirmedCount"].map(lambda x: x >=100 )].plot( ax=ax,color = "#73181b");
    plt.title(fileName, fontsize = 16);

    # plt.show()
    plt.savefig("static/figs/" + fileName,dpi=300)

def make_ch_map_from_data(data,fileName):
    

    print("geo coding...")
    geo_code_dict = load_geo_code_dict()
    geo_coding(data,geo_code_dict,GEOLOCATOR)

    print("transfering to geo_data...")
    geo_code_dict = load_geo_code_dict()
    geo_data = tansferxy2geopandas(data,geo_code_dict)

    print("saving geo point data ...")
    # FIXME:
    geo_data.to_file("static/data_with_geo_point/" + fileName+ ".geojson",driver='GeoJSON',encoding="utf-8")

    print("loading and making maps...")
    china_map,city_map = load_base_map()
    joined_data = city_sjoin(city_map,geo_data)

    print("saving plolygon data...")

    joined_data.to_file("static/data_with_geo_polygon/" + fileName+ ".geojson",driver='GeoJSON',encoding="utf-8")

    make_ch_map(china_map,joined_data,fileName)


# ----------
if __name__ == '__main__':
    
 
   
    
    path = "static/data/"

    while True:
        i = 1
        with open("process.log","r") as f:
            temp = f.read()
        alread_set = temp.split("\n")

        for fileName in os.listdir(path):
            if "province" in fileName:
                continue
            if fileName in alread_set:
                i+=1
                continue
            
            print("reading data...",fileName,i)



            data = pd.read_csv(path + fileName,encoding='utf-8')
            make_ch_map_from_data(data,fileName.split(".")[0])
            i+=1
            with open("process.log","a") as f:
                f.write(fileName)
                f.write("\n")

        time.sleep(20)

       
            
        

