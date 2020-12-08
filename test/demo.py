import requests
import json
import os
from pathlib import Path
import getpass
from colorama import Fore, init
import platform
# 初始化颜色控制
init(autoreset=True)


class AutoLogin:

    def __init__(self):

        # 登录地址
        self.login_url = "http://172.16.202.201:804/srun_portal_pc.php?ac_id=1&"
        # 设置代理
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
        }
        self.username = None
        self.password = None
        # self._cookies = None
        self.cookies = {}
        # self.s = requests.Session()
        # 用户信息缓存地址
        self._path = None
        # 用户网络使用信息
        self.online_info = None
        # 使用平台
        self.platform = platform.system()

    @property
    def path(self):
        if self._path is None:
            if self.platform == "Linux":
                path_dir = Path("./.auto_login")
            else:
                path_dir = Path(os.getenv("APPDATA")) / ".auto_login"
            if not path_dir.exists():
                path_dir.mkdir(parents=True)
            self._path = path_dir / "auto_login_data.json"
        return self._path

    @property
    def flow(self):
        if self.online_info and isinstance(self.online_info, list):
            return round(float(self.online_info[0]) / (pow(1024, 3)), 4)
        return None

    def login(self):
        """选择课程
        """
        data = {
            "action": "login",
            "ac_id": 1,
            "user_ip": "",
            "nas_ip": "",
            "user_mac": "",
            "url": "",
            "username": self.username,
            "password": self.password
        }

        response = requests.post(self.login_url,
                                 data=data,
                                 headers=self.headers)
        self.cookies = response.cookies.get_dict()
        flag = self.cookies.get("login", None)
        if flag:
            # 登录成功,打印登录信息
            self.get_online_info()
            return True
        else:
            # 登录失败
            return False

    def get_online_info(self):
        # var k = Math.floor(Math.random() * ( 100000 + 1));
        k = 86063
        info_url = "http://172.16.202.201:804/include/auth_action.php?k=86063"
        data = {
            "action": "get_online_info",
            "key": k
        }
        response = requests.post(info_url,
                                 data=data,
                                 headers=self.headers,
                                 cookies=self.cookies)
        self.online_info = response.text.split(",")

    def login_out(self):
        # 只要输入一个错误的密码,则会被服务器自动强制下线(即使你在登录状态)
        # 给一个错误的密码
        self.username = "keluokeluode(✺ω✺)"
        self.password = "keluokeluode(✺ω✺)"
        self.login()

    def reset_login_info(self, username: str, password: str):
        self.username = username
        self.password = password

    def save_login_info(self):
        data = {
            "username": self.username,
            "password": self.password
        }
        data = json.dumps(data)
        self.path.write_text(data, encoding='utf-8')

    def load_login_info(self):
        if self.path.is_file():
            data = self.path.read_text(encoding='utf-8')
            data = json.loads(data)
            if isinstance(data, dict):
                self.username = data.get("username", None)
                self.password = data.get("password", None)
                return True
        return False

    def clear_login_info(self):
        if self.path.is_file():
            self.path.unlink()


class Menu:

    def __init__(self):

        self.menu = [
            "1. 登录(保存用户名密码)",
            "2. 登录(仅一次)",
            "3. 登出",
            "4. 清除登录信息",
            "q. 退出脚本"
        ]

    def print_menu(self):
        for chooice in self.menu:
            print(chooice)


def main():

    menu = Menu()
    aul = AutoLogin()
    while True:
        try:
            print(Fore.YELLOW + "自动上网脚本by网络部".center(30, "*"))
            menu.print_menu()
            user_input = input(">>>")
            if user_input == "1":
                if not aul.load_login_info():
                    username = input("请输入用户名:")
                    password = getpass.getpass("请输入密码:")
                    aul.reset_login_info(username, password)
                if aul.login():
                    aul.save_login_info()
                    print("".center(30, "#"))
                    print(Fore.GREEN + f"登录成功,已用流量: {aul.flow} GB")
                    print("".center(30, "#"))
                else:
                    print("".center(30, "#"))
                    print(Fore.RED + "登录失败,请检查用户名或密码是否正确")
                    print("".center(30, "#"))
            elif user_input == "2":
                username = input("请输入用户名:")
                password = getpass.getpass("请输入密码:")
                aul.reset_login_info(username, password)
                if aul.login():
                    print("".center(30, "#"))
                    print(Fore.GREEN + f"登录成功,已用流量: {aul.flow} GB")
                    print("".center(30, "#"))
                else:
                    print("".center(30, "#"))
                    print(Fore.RED + "登录失败,请检查用户名或密码是否正确")
                    print("".center(30, "#"))
            elif user_input == "3":
                aul.login_out()
                print("".center(30, "#"))
                print(Fore.GREEN + "注销成功")
                print("".center(30, "#"))
            elif user_input == "4":
                aul.clear_login_info()
                print("".center(30, "#"))
                print(Fore.GREEN + "信息清除成功")
                print("".center(30, "#"))
            elif user_input == "q":
                return
            else:
                print("".center(30, "#"))
                print(Fore.RED + "请输入正确的选项,(๑′ᴗ‵๑)Ｉ Lᵒᵛᵉᵧₒᵤ❤")
                print("".center(30, "#"))
        except Exception as e:
            print("".center(30, "#"))
            print(Fore.RED + "发生了点意外~")
            print(f"错误信息: {e}")
            print("".center(30, "#"))


if __name__ == "__main__":

    main()
