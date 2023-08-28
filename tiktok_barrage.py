import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config as conf
import time
import random

executor = concurrent.futures.ThreadPoolExecutor(max_workers=len(conf.user_account))


class Send_Barrage:

    def __init__(self, Group, driver, username):
        self.url = 'https://live.douyin.com/{}'.format(conf.live_id)
        self.driver = driver
        self.username = username
        self.textarea = None
        self.group = Group

    def openLive(self, cookies):
        self.initLive(cookies)

        self.textarea = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='与大家互动一下...']"))
        )


        if self.textarea is None:
            conf.logger.error("{} 的直播界面错误".format(self.username))
            return False
        return True

    def initLive(self, cookies):
        self.driver.get(self.url)
        time.sleep(3)
        # for cookie in cookies:
        #     cookie_dict = {
        #         'domain': '.douyin.com',
        #         'name': cookie.get('name'),
        #         'value': cookie.get('value'),
        #         'expires': cookie.get('expiry'),
        #         'path': '/',
        #         'httpOnly': False,
        #         'HostOnly': False,
        #         'Secure': False
        #     }
        #     self.driver.add_cookie(cookie_dict)
        # time.sleep(1)
        # self.driver.refresh()

    def sendBarrage(self, msg):
        self.textarea.clear()
        self.textarea.send_keys(msg)
        self.textarea.send_keys(Keys.ENTER)
        conf.logger.info("点赞成功")
        self.textarea.clear()

    def autoSend(self):
        barrageList = self.group.getBarrageList()
        n = len(barrageList)
        while True:
            if not self.group.IsAuto(): break
            breakTime = self.group.getBreakTime()
            random_index = random.randint(0, n - 1)
            barrage = barrageList[random_index]
            self.sendBarrage(barrage)
            time.sleep(breakTime)

    def start(self):
        if self.group.IsAuto():
            executor.submit(self.autoSend)


class Barrage_Group:

    def __init__(self, barrageList, breakTime, groupName, isAuto):
        self.barrageList = barrageList
        self.breakTime = breakTime
        self.groupName = groupName
        self.isAuto = isAuto

    def addBarrage(self, barrage):
        self.barrageList.append(barrage)

    def getBarrageList(self):
        return self.barrageList

    def getBreakTime(self):
        return self.breakTime

    def getGroupName(self):
        return self.groupName

    def IsAuto(self):
        return self.isAuto

    def enableAuto(self):
        self.isAuto = True

    def closeAuto(self):
        self.isAuto = False


groupType = {
    "Genius": Barrage_Group(["12345", "主播你好1", "6666666","困了","鬼来了"], 3, "Genius", True)
}
