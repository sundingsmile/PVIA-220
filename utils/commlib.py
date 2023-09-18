'''
coding:utf-8
@Software: 将测试数据导入
@Time:2023/8/18 
@Author: Smile
'''

import yaml,os

'''导入测试数据'''
def data_init():
    with open('./data/data_dev.yaml') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
        # 读取要用的测试数据
        final_data = [(data['username'], data['password'], data['expected']['response']) for data in data['login']]
    return final_data

'''导入环境信息'''
def env_init():
    with open('./config/test/config.yaml') as f:
        url = yaml.load(f, Loader=yaml.SafeLoader)
    return url['host']['url']



def cc():
    global s
    print(s)
    print('/'*30)