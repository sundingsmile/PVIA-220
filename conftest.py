'''
coding:utf-8
@Software:
@Time:2023/8/11 
@Author: Smile
'''

'''
=================================================
pytest通用夹具
=================================================
'''
import pytest

@pytest.fixture(scope='function',params=['A','B','C'],ids=('敌法师','you','he'),name='sunding')
def practice_me(request):
    print('夹具测试，测试用例前置，全局')
    yield request.param
    print('测试夹具，测试用例后置，全局')


'''
=================================================
pytest通用配置项
=================================================
'''

import os,yaml

'''在命令行中定义输入参数'''
def pytest_addoption(parser):
    parser.addoption("--env",
                     action="store",
                     dest="environment",
                     default="test",
                     help="environment: test or prod or dev")


'''获取输入参数，根据输入参数组成不同地址，实现根据参数不同选择不同配置文件'''
@pytest.fixture(scope="session")
def env(pytestconfig):
    config_path = os.path.join(pytestconfig.rootdir,"config",pytestconfig.getoption('--env'),"config.yaml")
    with open(config_path) as f:
        env_config = yaml.load(f, Loader=yaml.SafeLoader)
    return env_config

'''另外一种实现方式实现上面所说功能'''
# @pytest.fixture(scope="session")
# def env(request):
#     config_path = os.path.join(request.config.rootdir,"config",request.config.getoption('environment'),"config.yaml")
#     with open(config_path) as f:
#         env_config = yaml.load(f, Loader=yaml.SafeLoader)
#     return env_config

# '''根据--env输入参数，选择测试数据；还不能使用，由于不知道怎么将夹具中返回的数据应用到pytest.mark.parametrize中'''
# @pytest.fixture(scope='session',autouse=True)
# def data(pytestconfig):
#     if pytestconfig.getoption('--env') == 'test':
#         data_path = os.path.join(pytestconfig.rootdir, "data", pytestconfig.getoption('--env'), "data_dev.yaml")
#     elif pytestconfig.getoption('--env') == 'dev':
#         data_path = os.path.join(pytestconfig.rootdir, "data", pytestconfig.getoption('--env'), "data_in_dev.yaml")
#     elif pytestconfig.getoption('--env') == 'prod':
#         data_path = os.path.join(pytestconfig.rootdir, "data", pytestconfig.getoption('--env'), "data_in_prod.yaml")
#     else:
#         data_path = None
#         print('请正确输入参数【"test","dev","prod"】')
#     with open(data_path) as f:
#         data = yaml.load(f, Loader=yaml.SafeLoader)
#         final_data = [(data['username'], data['password'], data['expected']['response']) for data in data['login']]
#     return final_data





'''
=================================================
pytest-html报告优化配置
=================================================
'''
from py._xmlgen import html
from datetime import datetime
from pytest_metadata.plugin import metadata_key
from _pytest.config import Config
from configparser import ConfigParser

'''读取配置文件信息'''
setting_content = ConfigParser()
setting_content.read('./pytest.ini',encoding='UTF-8')

'''
    1、修复pytest-html文件中文乱码问题
    2、注意：如果想此处起作用，还需修改D:\\Program Files\\python3.9.13\\Lib\\pathlib.py文件中的write_text函数的编码为UTF-8,
        def write_text(self, data, encoding=None, errors=None):
        """
        Open the file in text mode, write to it, and close the file.
        """
        if not isinstance(data, str):
            raise TypeError('data must be str, not %s' %
                            data.__class__.__name__)
        with self.open(mode='w', encoding='UTF-8', errors=errors) as f:
            return f.write(data)
'''
def pytest_itemcollected(item):
    # 把case中的三引号注释输出到输出中的用例列表
    item._nodeid = item._nodeid.encode("UTF-8").decode("UTF-8")

'''显示环境信息'''
def pytest_configure(config):
    Config._metadata = config.stash[metadata_key]  # 防止提示没有_metadata属性报错
    config._metadata.pop("JAVA_HOME") # 删除java_home
    config._metadata["项目名称"] = setting_content['myself_pytest_html_config']['project_name'] # 添加项目名称

'''更改pytest-html测试报告名称'''
def pytest_html_report_title(report):
    report.title = setting_content['myself_pytest_html_config']['report_title']

'''修改summary总结内容'''
def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([html.p("所属部门：{}".format(setting_content['myself_pytest_html_config']['tester_department']))])
    prefix.extend([html.p("测试人员：{}".format(''.join(setting_content['myself_pytest_html_config']['tester'])))])
#
'''修改result表头'''
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th("用例描述"))
    cells.insert(3, html.th('执行时间'))
    cells.remove(html.th('Links'))
    cells.remove(html.th('Duration'))
#
'''修改result表格的行'''
# def pytest_html_results_table_row(report, cells):
#     cells.insert(2, html.td(report.description))  # 插入用例描述
#     cells.insert(3, html.td(datetime.now(),class_="col-time"))  # 插入时间
#     cells.pop()  # 删除Links行
#     cells.pop()  # 删除Duration行

'''收集测试用例介绍，并且解决测试用例名称中包含中文乱码问题'''
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item,call): # Description取值为用例说明__doc__
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    report.nodeid = report.nodeid.encode("UTF-8").decode()  # 解决pytest-html生成的html报告中中文乱码问题



