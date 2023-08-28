from tiktok_login import TikTokLogin
from tiktok_barrage import Send_Barrage
import time
import pickle
import random
import config as conf
from config import logger
from tiktok_barrage import groupType


class TikTok_User:

    def __init__(self, username, password, user_group):
        self.room_url = 'https://live.douyin.com/{}'.format(conf.live_id)
        self.username = username
        self.password = password
        self.user_group = user_group
        self.is_login = False
        self.driver = conf.getWebDriver()
        self.barrage = Send_Barrage(groupType.get(str(user_group)), self.driver, self.username)
        self.cookies = None

    def userLogin(self):
        login = TikTokLogin(self.username, self.password, self.driver)
        self.is_login = login.login()
        self.cookies = login.getCookie()

    def isLogin(self):
        if self.is_login:
            return True
        logger.error("{}请先登录".format(self.username))
        return False

    def openLive(self):
        if self.isLogin():
            logger.info('{} 进入直播间...'.format(self.username))
            return self.barrage.openLive(self.cookies)
        return False

    def sendBarrage(self):
        if self.openLive():
            while True:
                barrage = input("输入弹幕")
                if barrage == 'ECS':
                    break
                self.barrage.sendBarrage(barrage)

    def autoBarrage(self):
        if self.openLive():
            logger.info("{}自动发送将于5s后启动".format(self.username))
            time.sleep(5)
            self.barrage.start()
