import requests

login_url = "http://172.16.202.202/srun_portal_pc?ac_id=39&theme=bnu"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
}

# postdata = {
#     "action": "#",
#     "nas_ip": "",
#     "user_mac": "",
#     "url": "",
#     "ac_id":39,
#     "domain":"",
#     "double_stack":0,
#     "user_ip":"",
#     "ip":"",
#     "otp":"true",
#     "password":131813,
#     "username":11312019220
# }

postdata={
    "ac_id":39,
    "action":"login",
    "chksum":"cee86264600b5324a54a1cd4222fad9f867b9b67",
    "double_stack":0,
    "info":"{SRBX1}vP0Sc1u6F/XVQc5JcWfb9l2FY1ruXK7DCPbcWswwXDsip7pmqKs5uLYbjBZ1pPAwYqa60ITNDJQne4jrWgXbM4JmuTrIst6beZM/fvs9MnPR8yMQqu7TQAu9O2AdNc4L/GbnWpQaUb+=",
    "ip":"172.24.71.145",
    "n":200,
    "name":"Windows",
    "os":"Windows 10",
    "password":"{MD5}5a448633db00a415ef8e133dd9f64831",
    "type":1,
    "username":"11312019220"
}


# postdata={
#     "ac_id":39,
#     "action":"login",
#     "chksum":"",
#     "double_stack":0,
#     "info":"",
#     "ip":"",
#     "n":200,
#     "name":"",
#     "os":"",
#     "password":"131813",
#     "type":1,
#     "username":"11312019220"
# }

responseRes = requests.post(login_url,
                            data=postdata,
                            headers=headers)
cookies = responseRes.cookies.get_dict()
print(cookies)
# print(responseRes.text)
