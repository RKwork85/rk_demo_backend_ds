import requests 

with requests.put('http://127.0.0.1:5000/dataset/1?instruction=1111&output=123456') as res:
    print(res.json())


