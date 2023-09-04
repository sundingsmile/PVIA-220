'''
coding:utf-8
@Software: 执行脚本运行命令开始执行脚本
@Time:2023/9/4 
@Author: Smile
'''

import pytest,os,json

'''
=================================================
allure报告配置，修改allure报告名称
=================================================
'''
def get_report_dir():
    current_dir = os.getcwd()
    report_dir = os.path.join(current_dir, r'report\allure_report\html-report\widgets\summary.json')
    with open(report_dir,encoding='utf-8',mode='r+') as f:
        ss =  json.load(f)
        ss['reportName'] = '中国万岁'
        f.seek(0)
        json.dump(ss,f,ensure_ascii=False, indent=4)

if __name__ == '__main__':

    '''
    =================================================
    pytest两种执行方式
    -m smoke 根据设置的关键字进行运行（@pytest.mark.smoke）
    --reruns=2 设置出错重跑
    -W ignore 忽略警告
    --env=test 执行测试环境配置信息，跟conftest.py脚本中内容相关
    PVIA_220_PYTEST_AUTO.py::Test_PVIA_220_MODIFY_230818::test_test 执行指定类中的测试
    -vs 显示具体执行过程，打印脚本中的打印信息
    =================================================
    '''
    # os.system('pytest -vs --env=test ./PVIA_220_PYTEST_AUTO.py -W ignore --reruns=2 -m smoke')
    # pytest.main(['-vs','--env=test','./PVIA_220_PYTEST_AUTO.py', '-W ignore','--reruns=2','-m smoke'])

    '''
    =================================================
    生成pytest_html报告
    ================================================
    '''
    # os.system('pytest --html=./report/report_name.html PVIA_220_PYTEST_AUTO.py::Test_PVIA_220_MODIFY_230818::test_test')

    '''
    =================================================
    生成allure报告
    =================================================
    '''
    # pytest.main(['-vs','./','--html=../report/pytest_html_report/report.html','--capture=tee-sys'])
    os.system('pytest -vs --env=test ./TestCase/test_practice.py --alluredir  ./report/allure_report/temp')
    os.system('allure  generate ./report/allure_report/temp -o ./report/allure_report/html-report --clean')
    get_report_dir()