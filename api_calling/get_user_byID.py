import requests 

with requests.get('http://127.0.0.1:5000/dataset/10') as res:
    print(res.json())


