'''
coding:utf-8
@Software:
@Time:2023/8/9 
@Author: Smile
'''
import datetime

# s = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
#
# print(type(s))
import os

import yaml

# yamlprint('=' * 20)


# with open('./data/data_in_test.yaml') as f:
#     data = yaml.load(f,Loader=yaml.SafeLoader)
#
# with    url = yaml.load(f,Loader=yaml.SafeLoader)
#  open('./config/test/config.yaml') as f:
#
# print(url['host']['url'])

# print(data)
# print(dat['age'])


class A():
    @classmethod
    def execute_function(cls, s):
        # 检查参数是否为函数名
        if isinstance(s, str):
            # 使用 eval 函数获取函数对象
            func = eval(s)
            # 检查函数对象是否存在
            if callable(func):
                # 执行函数
                func()
            else:
                print(f"Error: {s} is not a valid function")
        else:
            print("Error: Parameter must be a function name")


# from configparser import ConfigParser
# #
# # a = ConfigParser()
# #
# # s = a.read('../pytest.ini',encoding='UTF-8')
# # print(a.sections())
# #
# # print(a['myself_config']['tester'])

# class sunding:
#     def test(self):
#         print('test')
#
#     def __enter__(self):
#         print('__enter__')
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         print('__exit__')
#
#     def __call__(self, *args, **kwargs):
#         print('__call__')
#
#
# sunding()()

# import subprocess
#
# def find_command_path(command):
#     try:
#         # 执行系统命令 "where" 并获取输出
#         result = subprocess.run(['where', command], capture_output=True, text=True)
#         if result.returncode == 0:
#             # 提取命令的存放路径
#             path = result.stdout.strip().split('\n')[0]
#             return path
#         else:
#             print(f"Command '{command}' not found.")
#     except Exception as e:
#         print(f"Error: {e}")
# ss = find_command_path('allure')
# print(ss)

import json

# report_dir = r'D:\桌面\临时文件\python\PVIA-220\report\allure_report\html-report\widgets\summary.json'
# with open(report_dir,mode='r+',encoding='utf-8') as f:
#     dict = json.load(f)
#     dict['reportName'] = '牛逼克拉斯1'
#     print(dict)
#     f.seek(0)
#     json.dump(dict, f,ensure_ascii=False)

    # print(f.read())
    # dict1 = json.loads(f.read())


# with open(report_dir,mode='w',encoding='utf-8') as ff:
#     json.dump(dict,ff)


# import os
#
# current_dir = os.getcwd()
# parent_dir = os.path.dirname(current_dir)
#
# print("当前目录:", current_dir)
# print("父目录:", parent_dir)


import requests
from bs4 import BeautifulSoup
import time
import schedule

def get_train_info(date, from_station, to_station):
    url = f"https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={date}&leftTicketDTO.from_station={from_station}&leftTicketDTO.to_station={to_station}&purpose_codes=ADULT"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    result = response.json()
    trains = result["data"]["result"]
    for train in trains:
        train_info = train.split("|")
        print(f"车次：{train_info[3]}，出发站：{train_info[6]}，到达站：{train_info[7]}，出发时间：{train_info[8]}，到达时间：{train_info[9]}，余票：{train_info[20]}，票价：{train_info[23]}元")

def monitor_ticket_price():
    date = input("请输入查询日期（格式：yyyy-mm-dd）：")
    from_station = input("请输入出发站：")
    to_station = input("请输入到达站：")
    get_train_info(date, from_station, to_station)

def remind_ticket():
    # 在这里添加提醒用户购票的逻辑，例如发送邮件或者短信提醒
    pass
    print('=======')

schedule.every().day.at("10:54").do(monitor_ticket_price)

while True:
    schedule.run_pending()
    time.sleep(10)