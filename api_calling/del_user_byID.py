import requests 

with requests.delete('http://127.0.0.1:5000/dataset/4') as res:
    print(res.json())


