'''
coding:utf-8
@Software: PVIA_220_AUTO_TEST
@Time:2023/8/3 
@Author: Smile
'''
"""
XPATH使用教程
contains()：判断某个节点是否包含某个字符串
starts-with()：判断某个节点是否以某个字符串开头
text()：选取某个元素的文本
concat()：将多个字符串拼接为一个字符串
"""



import time,pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains


#  平台地址URL
pt_url = 'https://10.19.223.53/portal/'
username = 'ys'
password = 'Abc24680'

Chrome_ie = webdriver.Chrome()
Chrome_ie.maximize_window()
Chrome_ie.get(pt_url)
Chrome_ie.find_element(by = By.ID,value = 'details-button').click()
Chrome_ie.find_element(by = By.ID,value = 'proceed-link').click()
#  隐式等待
# Chrome_ie.implicitly_wait(10)
#  显示等待
WebDriverWait(Chrome_ie,10).until(EC.presence_of_element_located((By.XPATH,"//input[@placeholder='请输入密码']")))

#  登录业务
Chrome_ie.find_element(By.XPATH,"//input[@placeholder='请输入用户名']").send_keys(username)
Chrome_ie.find_element(By.XPATH,"//input[@placeholder='请输入密码']").send_keys(password)
Chrome_ie.find_element(By.XPATH,"//span[text()='登录']").click()

#  切换到iframe架构
WebDriverWait(Chrome_ie,10).until(EC.presence_of_element_located((By.XPATH,"//iframe[@name='frame_home']")))
Chrome_ie.switch_to.frame("frame_home")
WebDriverWait(Chrome_ie,20).until(EC.presence_of_element_located((By.ID,'cardimap_0000')),"定位不到电子地图")
Chrome_ie.switch_to.default_content()

'''智能搜索'''

#  1、进入智能搜索页面
move_mouse = ActionChains(Chrome_ie)
move_mouse.move_to_element(Chrome_ie.find_element(By.XPATH,"""//span[contains(text(),"智能搜索") and @class='first-menu-title']"""))
move_mouse.perform()
Chrome_ie.find_element(By.CSS_SELECTOR,"div#menuDropWrap-isearch_search_0>span.more-first-level-title[title='智能搜索']").click()

#  2、输入内容进行搜索
Chrome_ie.switch_to.frame('isearch_search_0')
Chrome_ie.find_element(By.CSS_SELECTOR,'input.el-input__inner[type="text"]').send_keys("白色上衣")
Chrome_ie.find_element(By.CSS_SELECTOR,'div[class $= search-button-color]').click()
Chrome_ie.switch_to.default_content()
time.sleep(20)



