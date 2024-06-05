# # 这个是登录用户

# import requests  
# import json  
  
# login_url = 'http://localhost:5000/login'  # 替换为你的服务器地址和端口  
# data = {  
#     'uuid':'rkkk'
# }  
# headers = {'Content-Type': 'application/json'}  
  
# resp = requests.post(url=login_url,data=json.dumps(data), headers=headers)
# print(resp.json())


# post_url = 'http://localhost:5000/dataset'  # 替换为你的服务器地址和端口  
# data = {  
#     'instruction':'你好',  
#     'output': '哈哈哈哈哈哈sd这样？sadasasdasd',
#     'uuid': 'rkwork'
# }  
# headers = {'Content-Type': 'application/json'}  
  
# resp = requests.post(url=post_url,data=json.dumps(data), headers=headers)
# print(resp.json())

import requests
import json

# 登录
login_url = 'http://localhost:5000/login'  # 替换为你的服务器地址和端口
login_data = {
    'uuid': 'rkkk'
}
login_headers = {'Content-Type': 'application/json'}

login_resp = requests.post(url=login_url, data=json.dumps(login_data), headers=login_headers)
login_json = login_resp.json()
print("登录响应:", login_json)

# 获取 session 信息
uuid = login_resp.cookies.get('uuid')
print("uuid ID:", uuid)

# 发送数据
post_url = 'http://localhost:5000/dataset'  # 替换为你的服务器地址和端口
post_data = {
    'instruction': '你好',
    'output': '哈哈哈哈哈哈sd这样？sadasasdasd',
    'uuid': 'rkwork'
}
post_headers = {
    'Content-Type': 'application/json',
    'Cookie': f'uuid={uuid}'
}

post_resp = requests.post(url=post_url, data=json.dumps(post_data), headers=post_headers)
post_json = post_resp.json()
print("数据发送响应:", post_json)