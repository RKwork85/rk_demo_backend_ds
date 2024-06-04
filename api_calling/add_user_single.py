# 这个是注册用户

import requests  
import json  
  
url = 'http://localhost:5000/dataset'  # 替换为你的服务器地址和端口  
data = {  
    'instruction':'你好',  
    'output': '我是广州阿斯加德莱克斯顿就看见阿拉萨吉拉拉吉林省拉德季拉丝机到啦萨达撒娇漏打卡'  
}  
headers = {'Content-Type': 'application/json'}  
  
resp = requests.post(url=url,data=json.dumps(data), headers=headers)
print(resp.json())

