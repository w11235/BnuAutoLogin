# import hashlib
# "a2095d7a81b106b5f644937b07f0eeaa"
# token = 'ba5329d5865ec4fcef3c5dd0011c21b79538981c0aadd72b343761208650c361'
# password = 'qqwert1123'

# m2 = hashlib.md5(token.encode('utf8'))
# m2.update(password.encode('utf8'))
# print(m2.hexdigest())

import execjs
import base64
import json
# ctx = execjs.compile(open('jquery.md5.js').read())
# print(ctx.eval('md5("qqwert1123", "ba5329d5865ec4fcef3c5dd0011c21b79538981c0aadd72b343761208650c361")'))
# ctx = execjs.compile(open('test3.js').read())
# print(ctx.eval('add(1,2)'))


ctx = execjs.compile(open('min.js').read())
print(ctx.eval('$.base64.setAlpha("123")'))
# print(base64.b64encode(b'test',
#                        altchars='LVoJPiCN2R8G90yg+hmFHuacZ1OWMnrsSTXkYpUq/3dlbfKwv6xztjI7DeBE45QA').decode())
# print(json.dumps('test'))
# print(ctx.eval(
#     'xEncode({"username": "11231"},"ba5329d5865ec4fcef3c5dd0011c21b79538981c0aadd72b343761208650c361")'))

# print(str({'username': '1123'}))
