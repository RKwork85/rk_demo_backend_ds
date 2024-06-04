# 这个是走后门的接口用户
import requests

url = "http://127.0.0.1:5000/rkwork/register"
params = {
    "username": "mzui",
    "password": "muzi"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print(data["msg"])
else:
    print(f"Error: {response.status_code} - {response.text}")