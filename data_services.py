from flask import Flask, send_file, send_from_directory,make_response
import os
import json
import pandas as pd
app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

@app.route('/')
def index():
    return 'Index Page'


@app.route("/download/<filename>", methods=['GET'])
def download_file(filename):
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    directory = os.getcwd()  # 假设在当前目录
    return send_from_directory(directory+ "/static/data", filename)

@app.route('/data/<filename>')
def get_data(filename):

    directory = os.getcwd()  # 假设在当前目录
    print(directory)
    data = pd.read_csv(directory + "/static/data/%s"%filename)
    data = data.to_dict()
    return data

@app.route('/data/point/<filename>')
def get_geo_point(filename):

    directory = os.getcwd()  # 假设在当前目录
    print(directory)

    with open(directory + "/static/data_with_geo_point/%s"%filename,"r",encoding="utf-8") as f:
        temp = f.read()
    data = json.loads(temp)
    # data = data.to_dict()
    return data

@app.route('/data/polygon/<filename>')
def get_geo_polygon(filename):

    directory = os.getcwd()  # 假设在当前目录
    print(directory)

    with open(directory + "/static/data_with_geo_polygon/%s"%filename,"r",encoding="utf-8") as f:
        temp = f.read()
    data = json.loads(temp)
    # data = data.to_dict()
    return data

@app.route("/download/point/<filename>", methods=['GET'])
def download_file_point(filename):
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    directory = os.getcwd()  # 假设在当前目录
    return send_from_directory(directory+ "/static/data_with_geo_point", filename)

@app.route("/download/polygon/<filename>", methods=['GET'])
def download_file_polygon(filename):
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    directory = os.getcwd()  # 假设在当前目录
    return send_from_directory(directory+ "/static/data_with_geo_polygon", filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
