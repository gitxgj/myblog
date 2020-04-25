import requests
import json

url = "http://127.0.0.1:8000/register/"

json_data = {
        'username': 'laowang',
        'password': '123456',
    }
requests.post(url=url, data=json_data)
