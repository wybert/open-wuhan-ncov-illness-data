# open-2019-ncov

这个项目有关有关 `武汉肺炎` `2019-ncov`的相关病例数据的分享。从[gitlab](https://gitlab.com/wybert/open-2019-ncov)迁移过来~。发布页[这里](https://wybert.github.io/open-wuhan-ncov-illness-data/)



# 数据介绍

该数据是从[丁香园·丁香医生](https://3g.dxy.cn/newh5/view/pneumonia?from=timeline&isappinstalled=0)通过爬虫获取的全国`2019-ncov`病毒的感染病例。

- 时间的分辨率：每一小时抓取一次
- 空间分辨率：城市、省份、国家
- 起止时间：对于城市和省粒度的数据从2020-1-25 15时到疫情结束。对于国家粒度的数据从2020-1-27 10时到疫情结束
- 数据缺失 2020-1-28 00到2020-1-28 12(由于程序中断，数据缺失这部分数据缺失)
- 数据缺失 对于2020-1-27 10到2020-1-29 19缺少部分省份的数据

# 数据下载和访问方法

## 获取json格式的数据

可以直接通过链接访问(对于构建应用的需求的可以使用这个方式)，返回数据形式为json，虽然url显示为`csv`。获取方法：


- 比如要获取`2020年1月25日15时`的各个城市粒度的病例数据，可以访问：`http://69.171.70.18:5000/data/city_level_2020-01-25T15.csv`

- 同理相同日期的省份或其他国家的数据可以访问：`http://69.171.70.18:5000/data/province_level_2020-01-25T15.csv`或`http://69.171.70.18:5000/data/country_level_2020-01-27T10.csv`

访问历史数据可以通过组装URL获得，比如`city_level_2020-01-25T15.csv`表示城市尺度的2010年1月15日15时的数据。按照从`00`到`23`小时（注意是两个零）。

### 应用程序示例

使用`python` `requests`模块

```python
import requests
import json
import pandas as pd
url = "http://69.171.70.18:5000/data/city_level_2020-01-25T15.csv"
response = requests.get(url)
data = json.loads(response.text)
dataset = pd.DataFrame(data)
```


## 获取geojson格式的数据

该数据是由病例数据经过百度地理编码得到，是地理编码后得到的坐标点的数据。获取地理数据的方式通过请求相应的URL得到，比如要访问2020-01-25日16时的点数据，可以通过下面的链接访问：

- 城市粒度：`http://69.171.70.18:5000/data/point/city_level_2020-01-25T16.geojson`
- 省粒度：`http://69.171.70.18:5000/data/point/province_level_2020-01-25T16.geojson`
- 国家粒度：`http://69.171.70.18:5000/data/point/country_level_2020-01-25T16.geojson`

> 注意：
> 1. 对于部分城市由于地名存在歧义，因此需要手工修改，因此地理数据有时可能不能得到实时的更新~
> 2. 虽然可以获得面装数据（如访问`http://69.171.70.18:5000/data/polygon/city_level_2020-01-25T16.geojson`），但是由于数据比较大，而且由于政治地理边界原因这里不推荐使用。



## 获取和下载csv表格数据

这种方法可以直接下载csv数据（确实是csv数据），该数据为utf无bom编码，对于Windows的excel来说，需要转换成utf含bom的编码方式。转换方法可以使用 notepad++完成（现在不需要了:）。比如要获取2020年1月25日15时的各个城市粒度的病例数据：

- 城市粒度：`http://69.171.70.18:5000/download/city_level_2020-01-25T15.csv`下载得到
- 省粒度：`http://69.171.70.18:5000/download/province_level_2020-01-25T15.csv`


## 下载geojson格式的数据

方式为：

- 城市粒度：`http://69.171.70.18:5000/download/point/city_level_2020-01-25T15.geojson`
- 省粒度：`http://69.171.70.18:5000/download/point/province_level_2020-01-25T15.geojson`
- 国家粒度：`http://69.171.70.18:5000/download/point/country_level_2020-01-25T15.geojson`


# R语言接口

[参考](https://github.com/microly/data2019ncov)

# 使用python完成分析

分析案例参考：[这里](https://gitlab.com/wybert/open-2019-ncov/blob/master/disasterMap.ipynb)

# 制图脚本

## 绘制每个小时的病例地图

`make_map.py`

## 制作视频

`make_video.py`

由于自己电脑内存太小，无法制作成视频分享给大家

# To do

- 构建github pages页面，发布可以下载数据的页面

# 使用该项目的项目

1. [武汉肺炎（2019-nCoV）数据的R语言接口](https://github.com/microly/data2019ncov)

# 引用


Xiaokang Fu, open-2019-ncov, Wuhan University, https://gitlab.com/wybert/open-2019-ncov

# 免责声明

- 本项目病例数据来源为：[丁香园·丁香医生](https://3g.dxy.cn/newh5/view/pneumonia?from=timeline&isappinstalled=0)
- 本项目地理编码使用[百度地理编码API完成](http://lbsyun.baidu.com/index.php?title=lbscloud/api/cloudrgc)
- 本项目地理面数据和行政边界来自于github:[china-geojson](https://github.com/yezongyang/china-geojson)
- 对于政治敏感的行政边界地图可以使用[高德提供的数据](http://datav.aliyun.com/tools/atlas)。

本人只负责整理数据，不承担任何法律责任。如有侵权请在微博私信[@Mayday大象](https://weibo.com/6324245960/profile) 

---


