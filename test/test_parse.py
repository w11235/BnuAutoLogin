import execjs
import requests
import json

# ctx = execjs.compile(open('base64.js').read())
# print(ctx.call('encode', 'test'))
# ctx = execjs.compile(open('verify.js').read())
# print(ctx.call('sha1', "I'm Persian."))

# 登录网址
LOGIN_URL = "http://172.16.202.202/cgi-bin/get_challenge"
# 挑战/应答校验码网址
CHALLENGE_URL = "http://172.16.202.202/cgi-bin/get_challenge"
# 代理信息
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
}


class Login:

    def __init__(self, username, password):

        self.username = username
        self.password = password
        # //TODO: 获取本地ip
        self.ip = "172.24.71.200"
        self.acid = 39
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
            'ip': '172.24.71.200'
        }
        challenge_response = requests.get(CHALLENGE_URL,
                                          params=challenge_data,
                                          json=True,
                                          headers=HEADER)
        crd = challenge_response.json()
        token = crd['challenge']
        # 获取密码的md5值
        password_hmd5 = self._get_password_hmd5(token)
        # 获取info值
        info = self._get_info(token)
        # 获取效验字符串
        chkstr = self._get_chkstr(token, password_hmd5, info)

        print('password_hmd5')
        print(password_hmd5)
        print('info')
        print(info)
        print('chkstr')
        print(chkstr)

        data = {
            'action': "login",
            'username': self.username,
            'password': password_hmd5,
            'ac_id': self.acid,
            'ip': self.ip,
            'chksum': chkstr,
            'info': info,
            'n': self.n,
            'type': self.type,
            'os': 'Windows 10',
            'name': "Windows",
            'double_stack': 0
        }
        login_response = requests.get(LOGIN_URL,
                                      #   data=data,
                                      params=data,
                                      json=True,
                                      headers=HEADER)
        print('login_response')
        print(login_response.text)
        print(login_response.cookies.get_dict())
        # s

    def _get_js_context(self, path):
        '''获取js上下文

        Args:
            path (str): js文件路径
        '''
        ctx = execjs.compile(open(path).read())
        return ctx

    def _get_password_hmd5(self, token: str)->str:
        '''获取密码的md5值

        Args:
            token (str): 挑战应答码

        Returns:
            str: password_hmd5
        '''
        verify_ctx = self._get_js_context('verify.js')
        js_str = f'md5("{token}","{self.password}")'
        hmd5 = verify_ctx.eval(js_str)
        password_hmd5 = "{MD5}" + hmd5
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
        # i = verify_ctx.eval(f'xEncode({str(i_dv)}, "{token}")')
        i = verify_ctx.call('xEncode', str(i_dv), token)
        print('i')
        print(i)
        info = "{SRBX1}" + base64_ctx.call('encode', i)
        return info

    def _get_chkstr(self, token, hmd5, info):
        '''获取效验字符串
        '''
        chkstr = token + self.username
        chkstr += token + hmd5
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
    password = 'qqwert1123'
    lg = Login(username, password)
    lg.login()
