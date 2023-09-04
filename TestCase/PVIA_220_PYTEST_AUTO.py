'''
coding:utf-8
@Software:
@Time:2023/8/7 
@Author: Smile
'''

import time,pytest,os,pyautogui,datetime,yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from pynput.keyboard import Controller
from utils import commlib



@pytest.mark.skip
class Test_PVIA_220():

    '''打印当前正在执行/要结束的测试用例'''
    @pytest.fixture()
    def setup(self,request):
        print('\n\r【' + '~'*20 + request.node.name + '任务正在执行' + '~'*20 +'】')
        yield
        print('\n\r【' + '~' * 20 + request.node.name + '任务已结束' + '~' * 20 + '】')



    '''浏览器初始化 + 登录平台'''
    @pytest.fixture()
    def fix_init_chrome(self,request):
        pt_url = 'https://10.19.223.53/portal/'
        username = 'ys'
        password = 'Abc24680'

        Chrome_ie = webdriver.Chrome()
        Chrome_ie.maximize_window()
        Chrome_ie.get(pt_url)
        Chrome_ie.find_element(by=By.ID, value='details-button').click()
        Chrome_ie.find_element(by=By.ID, value='proceed-link').click()
        #  隐式等待
        Chrome_ie.implicitly_wait(5)
        #  显示等待
        WebDriverWait(Chrome_ie, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='请输入密码']")))
        #  登录业务
        Chrome_ie.find_element(By.XPATH, "//input[@placeholder='请输入用户名']").send_keys(username)
        Chrome_ie.find_element(By.XPATH, "//input[@placeholder='请输入密码']").send_keys(password)
        Chrome_ie.find_element(By.XPATH, "//span[text()='登录']").click()

        #  切换到iframe架构
        WebDriverWait(Chrome_ie, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[@name='frame_home']")))
        Chrome_ie.switch_to.frame("frame_home")
        WebDriverWait(Chrome_ie, 20).until(EC.presence_of_element_located((By.ID, 'cardimap_0000')), "定位不到电子地图")
        Chrome_ie.switch_to.default_content()

        '''判断是否登录成功'''
        assert '演示用户' in Chrome_ie.page_source

        '''yield后面的在测试用例要关闭时会调用'''
        yield Chrome_ie
        Chrome_ie.quit()
        # Chrome_ie.close()



    '''智能搜索测试用例'''
    @pytest.mark.skip
    def test_smart_text_search(self,fix_init_chrome,setup,request):
        #  获取夹具返回的内容
        Chrome_ie = fix_init_chrome
        #  1、进入智能搜索页面
        move_mouse = ActionChains(Chrome_ie)
        move_mouse.move_to_element(
        Chrome_ie.find_element(By.XPATH, """//span[contains(text(),"智能搜索") and @class='first-menu-title']"""))
        move_mouse.perform()
        Chrome_ie.find_element(By.CSS_SELECTOR,
                               "div#menuDropWrap-isearch_search_0>span.more-first-level-title[title='智能搜索']").click()

        #  2、输入内容进行搜索
        Chrome_ie.switch_to.frame('isearch_search_0')
        Chrome_ie.find_element(By.CSS_SELECTOR, 'input.el-input__inner[type="text"]').send_keys("白色上衣")
        Chrome_ie.find_element(By.CSS_SELECTOR, 'div[class $= search-button-color]').click()
        Chrome_ie.switch_to.default_content()

        #  3、根据返回内容进行截图
        Chrome_ie.switch_to.frame('isearch_search_0')
        assert WebDriverWait(Chrome_ie,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div.high-light-title")),'搜索结果未显示完整')
        Chrome_ie.switch_to.default_content()
        Chrome_ie.get_screenshot_as_file('./Result/' + request.node.name + '_' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '_result.jpg')


    '''以脸搜脸查询测试用例'''
    @pytest.mark.usefixtures('fix_init_chrome','setup')
    def test_pic_face_search(self,request):

        Chrome_ie = request.getfixturevalue("fix_init_chrome")
        #  1、进入智能搜索首页
        ActionChains(Chrome_ie).move_to_element(Chrome_ie.find_element(By.XPATH,"//span[@class='first-menu-title' and contains(text(),'智能搜索')]")).perform()
        Chrome_ie.find_element(By.CSS_SELECTOR,"span.more-first-level-title[title='智能搜索']").click()

        #  2、进入以脸搜脸页面
        Chrome_ie.switch_to.frame('isearch_search_0')
        WebDriverWait(Chrome_ie,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div#cardsearch_7')))
        Chrome_ie.find_element(By.CSS_SELECTOR, 'div#cardsearch_7').click()
        Chrome_ie.switch_to.default_content()

        #  3、上传图片
        Chrome_ie.switch_to.frame('frame_isearch_search_7')
        WebDriverWait(Chrome_ie,20).until(EC.presence_of_element_located((By.CLASS_NAME,'list_wrap')))
        Chrome_ie.find_element(By.CLASS_NAME,'list_wrap').click()
        WebDriverWait(Chrome_ie, 20).until(EC.presence_of_element_located((By.XPATH,"//div[contains(text(),'点击面板或者拖拽人员图片至此处')]")))
        Chrome_ie.find_element(By.XPATH,"//div[contains(text(),'点击面板或者拖拽人员图片至此处')]").click()
        Chrome_ie.switch_to.default_content()

        #  4、选择文件
        time.sleep(2)
        pyautogui.press('shift')  #  切换成英文，防止下面内容输入错误
        Controller().type("D:\桌面\proxy.jpg")  #  如果路径不包含中文可以使用pyautogui.write(r'abc')，包含中文的话使用pynput模块进行处理
        pyautogui.press('enter',presses=2)

        #  5、选择分析完成的人脸信息
        Chrome_ie.switch_to.frame('frame_isearch_search_7')
        WebDriverWait(Chrome_ie, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class = 'h-img-snippets-thumbnail__original-wrapper h-img-view--bg-gray']")))
        assert len(Chrome_ie.find_elements(By.XPATH, "//div[@class = 'h-img-snippets-thumbnail__original-wrapper h-img-view--bg-gray']")) > 0,"请更换人脸图片，未检测到人脸"
        faces = Chrome_ie.find_elements(By.XPATH, "//div[@class = 'h-img-snippets-thumbnail__original-wrapper h-img-view--bg-gray']")
        '''选择多个人脸解析结果'''
        if len(faces)>5:
            for x in range(5): faces[x].click()
        else:
            for x in range(len(faces)): faces[x].click()
        '''等待选择人脸解析结果'''
        WebDriverWait(Chrome_ie,20).until(EC.presence_of_element_located((By.XPATH,"//button[@class='el-button el-button--primary']")))
        Chrome_ie.find_element(By.XPATH,"//button[@class='el-button el-button--primary']").click()
        Chrome_ie.switch_to.default_content()

        #  6、点击查询，查看查询结果
        Chrome_ie.switch_to.frame('frame_isearch_search_7')
        Chrome_ie.find_element(By.CSS_SELECTOR,"input.el-input__inner[aria-valuenow='75']").clear()
        Chrome_ie.find_element(By.CSS_SELECTOR, "input.el-input__inner[aria-valuenow='75']").send_keys('10')
        Chrome_ie.find_element(By.XPATH,"//button[@class='el-button search_but el-button--primary']").click()
        WebDriverWait(Chrome_ie,20).until(EC.presence_of_element_located((By.XPATH,"//div[@class='AT_Content-left']/span[@class='highlight'][text()>0]")))
        Chrome_ie.switch_to.default_content()
        time.sleep(5)
        Chrome_ie.get_screenshot_as_file('./Result/' + request.node.name + '_查询结果_' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '_result.jpg')

        #  7、导出查询结果
        '''选择导出全部'''
        Chrome_ie.switch_to.frame('frame_isearch_search_7')
        ActionChains(Chrome_ie).move_to_element(Chrome_ie.find_element(By.XPATH,"//button[@class='el-button el-button--default is-icon is-icon-text el-dropdown-selfdefine']")).perform()
        WebDriverWait(Chrome_ie,20).until(EC.presence_of_element_located((By.XPATH,"//li[@class='el-dropdown-menu__item' and contains(text(),'导出全部')]")))
        Chrome_ie.find_element(By.XPATH,"//ul[@class='el-dropdown-menu el-popper']/li[contains(text(),'导出全部')]").click()

        '''确定已经弹出导出页面'''
        WebDriverWait(Chrome_ie,20).until(EC.presence_of_element_located((By.XPATH,"//button[@class='el-button el-button--info']")))
        Chrome_ie.find_element(By.XPATH,"//button[@class='el-button el-button--info']").click()
        Chrome_ie.switch_to.default_content()

        Chrome_ie.get_screenshot_as_file('./Result/' + request.node.name + '_导出结果_' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '_result.jpg')


'''
登录测试用例，引入yaml文件将可变参数和测试用例进行解耦，
并且将平台地址这些信息也进行解耦，实现灵活变动
'''
class Test_PVIA_220_MODIFY_230818():

    '''登录测试用例'''
    # @pytest.mark.skip
    @pytest.mark.parametrize('username,password,expected',[('ys', 'Abc24680', '演示用户'), ('admin', 12345, '用户名或密码错误')])
    def test_login(self,username,password,expected,env):
        Chrome_ie = webdriver.Edge()
        Chrome_ie.maximize_window()
        Chrome_ie.get(env['host']['url'])
        Chrome_ie.find_element(by=By.ID, value='details-button').click()
        Chrome_ie.find_element(by=By.ID, value='proceed-link').click()
        #  隐式等待
        # Chrome_ie.implicitly_wait(5)
        #  显示等待
        WebDriverWait(Chrome_ie, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='请输入密码']")))
        #  登录业务
        Chrome_ie.find_element(By.XPATH, "//input[@placeholder='请输入用户名']").send_keys(username)
        Chrome_ie.find_element(By.XPATH, "//input[@placeholder='请输入密码']").send_keys(password)
        Chrome_ie.find_element(By.XPATH, "//span[text()='登录']").click()

        #  切换到iframe架构
        try:
            WebDriverWait(Chrome_ie, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[@name='frame_home']")))
            Chrome_ie.switch_to.frame("frame_home")
            WebDriverWait(Chrome_ie, 20).until(EC.presence_of_element_located((By.ID, 'cardimap_0000')), "定位不到电子地图")
            Chrome_ie.switch_to.default_content()
        except:
            WebDriverWait(Chrome_ie,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'i.lidaicon-warning-triangle-md-f')))
            assert expected in Chrome_ie.page_source
        else:
            '''判断是否登录成功'''
            assert expected in Chrome_ie.page_source




    '''验证问题专用程序'''
    # @pytest.mark.skip
    # @pytest.mark.usefixtures('env')
    # @pytest.mark.parametrize('a', )
    @pytest.mark.run(order=1)
    @pytest.mark.smoke
    def test_test(self):
        print('+'*15 + 'test_test' + '+'*15)
        print('&'*20)
        assert 0






if __name__ == "__main__":
    # os.system('pytest -vs ./PVIA_220_PYTEST_AUTO.py -m "sunding"')
    os.system('pytest -vs --env=test ./PVIA_220_PYTEST_AUTO.py -W ignore --reruns=2 -m smoke')
    pytest.main(['-vs','--env=test','./PVIA_220_PYTEST_AUTO.py', '-W ignore','--reruns=2','-m smoke'])
    # os.system('pytest --html=./report/report_name.html PVIA_220_PYTEST_AUTO.py::Test_PVIA_220_MODIFY_230818::test_test')
