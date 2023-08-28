from selenium import webdriver
from selenium.webdriver import Edge, EdgeOptions
from selenium.webdriver.chrome.options import Options
import logging
import os
from selenium.webdriver.remote.remote_connection import LOGGER

# 禁用Selenium远程连接的日志输出
LOGGER.setLevel(logging.WARNING)
options = EdgeOptions()
options.binary_location = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"  # 设置 Edge 浏览器的路径
# 配置日志
logging.basicConfig(
    # 指定日志文件的名称
    level=logging.DEBUG,   # 设置日志级别，可以是DEBUG, INFO, WARNING, ERROR, CRITICAL
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 创建一个Logger对象
logger = logging.getLogger('tiktok')
logger.addHandler(logging.StreamHandler())

user_account = [
    {
        'username': "xxxxxx",
        'password': 'xxxxxx',
        'group': "Genius"
    }
]

live_id = '350303043343'
douyin = 'https://www.douyin.com/'
timeout = 10
options = EdgeOptions()
options .add_argument("--disable-features=SameSiteByDefaultCookies")
options .add_argument("--disable-features=CookiesWithoutSameSiteMustBeSecure")
barrage_group = [

]
def getWebDriver():
    return Edge(options=options)
