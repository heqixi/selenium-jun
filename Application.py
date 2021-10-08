# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 03:18:17 2021

@author: Raytine
"""
import os
import unittest
import time, datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 读取账号的信息，然后登陆
# 读取要抢的箱子的起始和终止地理位置，在特定时间刷新，然后抢箱子
class Application(object):
    def __init__(self, params, ui):
        self.params = params
        self.ui = ui

    def run(self):
        self.test_cookie_allow_all_button_click()
    
    def start(self) -> None:
        startTime = self.params['task_start_time']
        while datetime.datetime.now() < startTime:
            self.ui.log('i', "离任务启动还有 %s 秒" %(startTime - datetime.datetime.now()))
            time.sleep(6)
            print("waiting for task start")
        self.ui.log('i', "任务启动")
        try:
            chrome_driver_path = './chromedriver.exe'
            options = webdriver.ChromeOptions()
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            #options.add_argument("--headless")
            options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')
            self.driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)
            #with open('D:\src\python\Web\stealth.min.js') as f:
                #    js = f.read()
                #self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                #    "source":js
            #})
            self.driver.implicitly_wait(30)
            self.driver.maximize_window()
            #self.driver.get("https://synconhub.coscoshipping.com/")
            self.driver.get("https://www.baidu.com/")
        except Exception as e:
            raise ClientException("启动浏览器失败", e)
        else:
            self.test_cookie_allow_all_button_click()  

    def test_cookie_allow_all_button_click(self):
        time.sleep(2)
        try:
            allow_all_btn = self.driver.find_element_by_css_selector("div.cookie-button > button.el-button.el-button--primary")
            ActionChains(self.driver).move_to_element(allow_all_btn).perform()
            ActionChains(self.driver).click(allow_all_btn).perform()
        except NoSuchElementException as e:
            self.ui.log("w", "no cookie dialog")
            time.sleep(2)
            self.login()
        else:
            self.login()

    def login(self):
        try:
            time.sleep(1)
            login_btn = self.driver.find_element_by_css_selector("div.auth-container")
            ActionChains(self.driver).move_to_element(login_btn).click(login_btn).perform()
            time.sleep(1)
            use_name_input = self.driver.find_element_by_css_selector("div.el-input.el-input--prefix > input[name='login_dialog_username']")
            use_name_input.send_keys(self.params["user_name"])
            time.sleep(2)
            password_input = self.driver.find_element_by_id("login-password-input")
            password_input.send_keys(self.params["password"])
            time.sleep(1)
            login_confirm_btn = self.driver.find_element_by_css_selector("div.btn-bar > button[name='login_dialog_btn_login']")
            ActionChains(self.driver).move_to_element(login_confirm_btn).click(login_confirm_btn).perform()
        except Exception as e:
            raise ClientException("登录失败", e)
        else:
            self.search_route()

    def search_route(self):
        try:
            wait = WebDriverWait(self.driver, 5)
            route_start = self.driver.find_element_by_css_selector("div.el-select.location-select > div.el-input.el-input > input.el-input__inner")
            route_start.send_keys(self.params["start_port_search_key"])
            ActionChains(self.driver).move_to_element(route_start).send_keys(Keys.DOWN).send_keys(Keys.ENTER).perform()
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".el-select-dropdown__item")))
            ## select dropdown list
            dropdown_div = self.driver.find_element_by_xpath('//li[@class="el-select-dropdown__item"]')
            candidate_start = self.driver.find_element_by_xpath("//span[contains(text(), '%s')]"%(self.params["start_port_match_key"]))
            ActionChains(self.driver).move_to_element(candidate_start).click(candidate_start).perform()
            #print(self.driver.find_element_by_xpath("//span[contains(text(), '上海-Shanghai')]"))

            ## 目的地
            route_dest_div = self.driver.find_element_by_xpath('//div[@class="ect-search-form-item"][last()]')
            route_dest_div_input = route_dest_div.find_element_by_tag_name("input")
            route_dest_div_input.send_keys(self.params["dest_port_search_key"])
            ActionChains(self.driver).move_to_element(route_dest_div_input).send_keys(Keys.DOWN).send_keys(Keys.ENTER).perform()

            #
            candidate_dest = self.driver.find_element_by_xpath("//span[contains(text(), '%s')]"%(self.params["dest_port_match_key"]))
            ActionChains(self.driver).move_to_element(candidate_dest).click(candidate_dest).perform()

            # 查询
            search_button = self.driver.find_element_by_css_selector("button[name='sailing_product_btn_search']")
            search_button.click()

            #self.go_to_buy_index_zero()
        except Exception as e:
            raise ClientException("搜索航线失败", e)

    def go_to_buy_index_zero(self):
        # 去购买
        buy_now = self.driver.find_element_by_css_selector("button[name='sailing_product_result_0_buy_action']")
        ActionChains(self.driver).move_to_element(buy_now).click(buy_now).perform()
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])

        #选择40HQ
        forty_hq_div = self.driver.find_element_by_xpath("//td[contains(text(), '%s')]/.."%(self.params["box_style"]))
        print(forty_hq_div.get_attribute("innerHTML"))
        #increase_button = forty_hq_div.find_element_by_css_selector("td.order_number > div.el-input-number > button > span.el-input-number__increase")
        #ActionChains(self.driver).move_to_element(increase_button).click(increase_button).perform()

class ClientException(Exception):
    def __init__(self, msg, ex):
        super().__init__(self)
        self.message = msg
        self.exception = ex
    def __str__(self):
        return self.message + "\n" + "%s"%(self.exception)

if __name__ == '__main__':
    params={"user_name":"HUA", "password":"asdf?135","start_port_search_key":"上海","start_port_match_key":"上海-Shanghai","dest_port_search_key":"汉堡","dest_port_match_key":"汉堡-Hamburg","box_style":"40HQ"}
    testCase = Application(params)
    testCase.start()
    testCase.test_cookie_allow_all_button_click()
    
    