import time

from tiktok_user import TikTok_User
import tiktok_login

account = tiktok_login.getAccount()

login_map = {}


if __name__ == '__main__':
    for userData in account:
        user = TikTok_User(userData['username'],userData['password'],userData["group"])
        user.userLogin()
        user.autoBarrage()
        input("按任意键继续...")









