# 这个是注册用户

import requests  
import json  
  
url = 'http://localhost:5000/dataset'  # 替换为你的服务器地址和端口  
data = {  
    'instruction':'你好',  
    'output': '哈哈哈哈哈哈sd这样？sadasasdasd',
    'uuid': 'rkwork'
}  
headers = {'Content-Type': 'application/json'}  
  
resp = requests.post(url=url,data=json.dumps(data), headers=headers)
print(resp.json())

