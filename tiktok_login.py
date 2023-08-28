import time
from config import logger
import config as conf
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
import json
import asyncio
import concurrent.futures
import functools

account_list = conf.user_account
executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)


def getAccount():
    return account_list


class TikTokLogin:

    def __init__(self, username, password, driver):
        # 实例变量
        self.username = username
        self.password = password
        self.driver = driver
        self.file_name = "./cookie/{}_cookie.json".format(self.username)
        self.loop = asyncio.get_event_loop()

    def getCookie(self):
        with open(self.file_name, "r") as file:
            data = json.load(file)
            return data[str(self.username)]

    def getLoginCookie(self):
        if os.path.exists(self.file_name):
            logger.info("已存在的用户{}cookie内容".format(self.username))
            self.loadCookie(self.getCookie())
            return True
        else:
            logger.info("{} 不存在登录文件，正在执行登录操作...".format(self.username))
            return False

    def getLoginPlantTable(self):
        self.driver.get(conf.douyin)
        wait = WebDriverWait(self.driver, conf.timeout)
        password_login_element = wait.until(EC.presence_of_element_located((By.XPATH, "//li[@aria-label='密码登录']")))
        password_login_element.click()

    def inputInfo(self):
        wait = WebDriverWait(self.driver, 10)
        phone_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='手机号']")))
        phone_input.click()
        phone_input.send_keys(self.username)

        # 找到密码输入框并点击输入内容
        password_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='请输入密码']")))
        password_input.click()
        password_input.send_keys(self.password)

        # 找到登录按钮并点击
        login_button = self.driver.find_element(By.XPATH, "//button[@class='web-login-button']")
        login_button.click()
        self.hasPhoneCheck()
        self.saveCookie()

    def hasPhoneCheck(self):
        try:
            i = 0
            while True:
                sms_container = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "second-sms-container"))
                )
                text = "检测到验证码" if i == 0 else '验证码错误'
                input_element = sms_container.find_element(By.XPATH, "//input[@aria-label='请输入验证码']")
                input_element.clear()
                verification_code = input("{}，请输入你的验证码(6位):".format(text))
                input_element.send_keys(verification_code)
                input_element.send_keys(Keys.RETURN)
                time.sleep(2)
                i += 1
        except Exception as e:
            logger.info("登录成功")

    def saveCookie(self):
        time.sleep(5)
        cookie = self.driver.get_cookies()
        data = json.dumps({self.username: cookie})
        executor.submit(functools.partial(self.saveCookieFile, data))

    def saveCookieFile(self, data):
        with open(self.file_name, "w") as json_file:
            json_file.write(data)
            logger.info('{}成功保存{}文件'.format(self.username, self.file_name))

    def loadCookie(self, cookies):
        self.driver.get(conf.douyin)
        time.sleep(1)
        for cookie in cookies:
            cookie_dict = {
                'domain': '.douyin.com',
                'name': cookie.get('name'),
                'value': cookie.get('value'),
                'expires': cookie.get('expiry'),
                'path': '/',
                'httpOnly': False,
                'HostOnly': False,
                'Secure': False
            }
            self.driver.add_cookie(cookie_dict)
        time.sleep(1)
        self.driver.refresh()

    def login(self):
        if self.getLoginCookie():
            return True
        else:
            try:
                self.getLoginPlantTable()
                self.inputInfo()
                return True
            except Exception as e:
                return False

    def getUsername(self):
        return self.username

    def getDriver(self):
        return self.driver
