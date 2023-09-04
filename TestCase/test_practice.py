'''
coding:utf-8
@Software: pytest练习
@Time:2023/8/23 
@Author: Smile
'''
import json

import allure
import pytest,os



# @pytest.fixture(scope='function',params=['A','B','C'],ids=('敌法师','you','he'),name='sunding')
# def practice_me(request):
#     print('夹具测试，测试用例前置')
#     yield request.param
#     print('测试夹具，测试用例后置')



# @allure.parent_suite('我是parent-suite')
# @allure.suite('我是suite')
# @allure.sub_suite('我是sub_suite')

# @allure.epic('我是epic')
# @allure.feature('我是feature')
# @allure.story('我是story')
#
# class TestA():
#     @allure.step('孙丁厉害')
#     @allure.title('我是tittle')
#     @pytest.mark.usefixtures('sunding')
#     def test_a(self,request):
#         '''test_a 测试用例描述'''
#         print('test_a')
#         print('=' * 20)
#         print(allure.severity_level.BLOCKER)
#         print(request.getfixturevalue('sunding'))
#         print('=' * 20)
#
#     def test_b(self,sunding):
#         print(sunding)
#         print('test_b')


class TestB():

    # @allure.id('我是id')
    # @allure.link('https://www.baidu.com',name='我是link')
    # @allure.label('我是label')
    # @allure.issue('https://home.firefoxchina.cn/?from=extra_start','我是issue')
    # @allure.description('我是description')
    # @allure.severity('blocker')
    # @allure.tag('我是tag')
    # @allure.testcase('https://sso.hikvision.com/login?service=http%3A%2F%2Fsso.hikvision.com.cn%2Fdomino%2FdominoLogin','我是testcase')
    # # @allure.description_html('我是description_html')
    # @allure.story('我是storyTESTB')
    # @allure.step('我是step-TESTB')
    # @pytest.mark.parametrize('a,b',[(1,1)])
    # def test_a(self,a,b):
    #     print('test_a')
    #     assert a == b

    @allure.step('什么东西，我理解不了')
    def test_b(self,request):
        print('test_b' + '===')
        # print(dir(request))
        # print(request.path)
        # print(request.node)
        # print(request.fspath)
        #
        # report_dir = os.path.join(request.path,r'report\allure_report\html-report\widgets\summary.json')
        #
        # print(report_dir)
        #
        # with open(report_dir,mode='w+',encoding='utf-8') as f:
        #     print(json.load(f))

# class TestC():
#     def test_a(self):
#         print('test_a')
#
#     def test_b(self):
#         print('test_b')
#         assert False

'''
=================================================
allure报告配置
=================================================
'''
def get_report_dir():
    current_dir = os.getcwd()
    parent_dir = os.path.dirname(current_dir)
    report_dir = os.path.join(parent_dir, r'report\allure_report\html-report\widgets\summary.json')
    with open(report_dir,encoding='utf-8',mode='r+') as f:
        ss =  json.load(f)
        ss['reportName'] = '中国万岁'
        f.seek(0)
        json.dump(ss,f,ensure_ascii=False, indent=4)


if __name__ == '__main__':
    # pytest.main(['-vs','./','--html=../report/pytest_html_report/report.html','--capture=tee-sys'])
    os.system('pytest -vs --env=test ./test_practice.py --alluredir  ../report/allure_report/temp')
    os.system('allure  generate ../report/allure_report/temp -o ../report/allure_report/html-report --clean')

    get_report_dir()
