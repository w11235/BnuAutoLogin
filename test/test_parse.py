import execjs
import requests
import json
# base64_ctx = execjs.compile(open('base64.js').read())
# print(ctx.call('encode', 'test'))

# 登录网址
LOGIN_URL = "http://gw.bnu.edu.cn/cgi-bin/srun_portal?callback=what'up man"
# 挑战/应答校验码网址
CHALLENGE_URL = "http://172.16.202.202/cgi-bin/get_challenge"
# 代理信息
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0', 'Connection': 'keep-alive'
}

s = requests.Session()


class Login:

    def __init__(self, username, password):

        self.username = username
        self.password = password
        # //TODO: 获取本地ip
        self.ip = "172.24.71.200"
        self.acid = '39'
        self.n = 200
        self.type = 1

    # @property
    # def cookies(self):
    #     self._cookies = response.cookies.get_dict()
    #     flag = self.cookies.get("login", None)

    def login(self):
        '''登录
        '''
        # 获取挑战/应答校验码
        challenge_data = {
            'username': self.username,
            'ip': self.ip,
        }

        challenge_response = s.get(CHALLENGE_URL,
                                   params=challenge_data,
                                   json=True,
                                   headers=HEADER)
        crd = challenge_response.json()
        token = crd['challenge']

        # 获取info值
        info = self._get_info(token)
        # 获取密码的md5值
        password_hmd5 = self._get_password_hmd5(token)
        # 获取效验字符串
        chkstr = self._get_chkstr(token, info)

        data = {
            'ac_id': self.acid,
            'action': "login",
            'chksum': chkstr,
            'info': info,
            'ip': self.ip,
            'n': self.n,
            'password': password_hmd5,
            'type': self.type,
            'username': self.username,
            # Next not important parameters
            'double_stack': 0,
            'name': "Windows",
            'os': 'Windows 10',
        }
        login_response = s.get(LOGIN_URL,
                               params=data,
                               headers=HEADER)
        print('login_response')
        print(login_response)
        print(login_response.text)
        # s

    def _get_js_context(self, path):
        '''获取js上下文

        Args:
            path (str): js文件路径
        '''
        ctx = execjs.compile(open(path).read())
        return ctx

    def _get_password_hmd5(self, token: str) -> str:
        '''获取密码的md5值

        Args:
            token (str): 挑战应答码

        Returns:
            str: password_hmd5
        '''
        verify_ctx = self._get_js_context('verify.js')
        self.hmd5 = verify_ctx.call('md5', self.password, token)
        password_hmd5 = "{MD5}" + self.hmd5
        return password_hmd5

    def _get_info(self, token: str):

        i_dv = json.dumps(
            {
                "username": self.username,
                "password": self.password,
                "ip": self.ip,
                "acid": self.acid,
                'enc_ver': "srun_bx1"
            }

        )
        verify_ctx = self._get_js_context('verify.js')
        base64_ctx = self._get_js_context('base64.js')
        i = verify_ctx.call('xEncode', i_dv.replace(' ', ''), token).encode(
            'gbk').decode('utf-8')
        info = "{SRBX1}" + base64_ctx.call('encode', i)
        return info

    def _get_chkstr(self, token, info):
        '''获取效验字符串
        '''
        chkstr = token + self.username
        chkstr += token + self.hmd5
        chkstr += token + str(self.acid)
        chkstr += token + self.ip
        chkstr += token + str(self.n)
        chkstr += token + str(self.type)
        chkstr += token + info
        verify_ctx = self._get_js_context('verify.js')
        chkstr = verify_ctx.call('sha1', chkstr)
        return chkstr


if __name__ == '__main__':

    username = '11312018303'
    password = ''
    lg = Login(username, password)
    lg.login()

    # import time
    # count = 5
    # while count >= 0:
    #     time.sleep(5)
    #     lg.login()
    #     count -= 1
