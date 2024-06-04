import requests 

with requests.get('http://127.0.0.1:5000/dataset') as res:
    print(res.json())


