'''
coding:utf-8
@Software: pytest练习
@Time:2023/8/23 
@Author: Smile
'''
import pytest


# @pytest.fixture(scope='module')
# def practice_me():
#     print('夹具测试，测试用例前置')
#     yield
#     print('测试夹具，测试用例后置')



class TestC():

    @pytest.mark.usefixtures('sunding')
    def test_c(self):
        print('test_c')
        print('='*20)
        print(self.__class__.__name__)
        print('=' * 20)

    def test_d(self,sunding):
        print('test_d')

# class TestB():
#     def test_a(self):
#         print('test_a')
#
#     def test_b(self):
#         print('test_b')

if __name__ == '__main__':
    pytest.main(['-vs','--reruns=2','./test_practic.py'])