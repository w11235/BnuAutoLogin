import json
import os
import socket
import time

import execjs
import requests
from dotenv import find_dotenv, load_dotenv

# 登录网址
LOGIN_URL = "http://gw.bnu.edu.cn/cgi-bin/srun_portal"
# 挑战/应答校验码网址
CHALLENGE_URL = "http://gw.bnu.edu.cn/cgi-bin/get_challenge"
# 代理信息
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0', 'Connection': 'keep-alive'
}
USER_INFO_URL = "http://gw.bnu.edu.cn/cgi-bin/rad_user_info"
LOGOUT_URL = "http://gw.bnu.edu.cn/cgi-bin/rad_user_dm"


class Login:

    def __init__(self, username, password):

        # 持久化链接
        self.requests = requests.Session()
        self.username = username
        self.password = password
        # //TODO: 获取本地ip
        # 获取主机名
        hostname = socket.gethostname()
        # 获取IP
        self.ip = socket.gethostbyname(hostname)

        # 自定义回调函数名称
        self.ccn = "What's up man"
        self.acid = '39'
        self.n = 200
        self.type = 1

    def login(self):
        '''登录
        '''
        # 获取挑战/应答校验码
        challenge_data = {
            'username': self.username,
            'ip': self.ip,
        }

        challenge_response = self.requests.get(CHALLENGE_URL,
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
            'callback': self.ccn,
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
        login_response = self.requests.get(LOGIN_URL,
                                           params=data,
                                           headers=HEADER)
        login_response_data = self._parse_response_data(login_response)
        print('登录成功')
        return login_response_data

    def logout(self):
        '''登出
        '''
        # 1 if portal.MacAuth else 0
        unbind = 0
        t = str(time.time()).split('.')[0]
        verify_ctx = self._get_js_context('verify.js')
        sign = verify_ctx.call('sha1', t+self.username+self.ip+str(unbind)+t)
        data = {
            'callback': self.ccn,
            'ip': self.ip,
            'time': t,
            'username': self.username,
            'unbind': unbind,
            'sign': sign
        }
        logout_response = self.requests.get(LOGOUT_URL,
                                            params=data,
                                            headers=HEADER)
        logout_info = self._parse_response_data(logout_response)
        print('注销成功')
        return logout_info

    def get_user_info(self):
        '''获取用户信息
        '''
        data = {
            'callback': self.ccn
        }
        user_info_response = self.requests.get(USER_INFO_URL,
                                               params=data,
                                               json=True,
                                               headers=HEADER)
        user_info = self._parse_response_data(user_info_response)
        # user_info存放了所有查询到的用户数据,目前仅返回登录的账号名、已用流量、网费余额
        return_user_info = {
            'username': user_info['user_name'],
            'sum_bytes': str(user_info['sum_bytes'] / 1000000000)+' GB',
            'user_balance': str(user_info['user_balance'])+' 元'
        }

        print('user_info')
        print(return_user_info)
        return return_user_info

    def _parse_response_data(self, response: 'requests.Response'):
        '''解析相应数据

        注意: 本身就是Json格式的数据不需要解析
        '''
        response_data = response.text
        if self.ccn not in response_data:
            raise ValueError('未接收到正确的请求数据')
        response_data = response_data.replace(self.ccn+'(', '')[:-1]
        response_data = json.loads(response_data)
        error = response_data['error']
        if error not in ['ok', 'logout_ok']:
            raise ValueError(f"请求参数错误,错误信息: {error}")
        return response_data

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

    load_dotenv(find_dotenv(), override=True)
    username = os.environ.get('username')
    password = os.environ.get('password')
    lg = Login(username, password)
    lg.login()
    lg.get_user_info()
    lg.logout()
