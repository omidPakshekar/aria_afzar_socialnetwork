import requests

import requests
endpoint = "http://127.0.0.1:8000/api/v1/accounts/login/"
psw = "amir1234"
data = {
    "username" : "omid6",
    "email" : "omid6@gmail.com",
    "password" : psw,
}

auth_response = requests.post( endpoint, data=data ) # HTTP request

if auth_response.status_code == 200:
    token = auth_response.json()['access_token']  
    endpoint = "http://localhost:8000/api/v1/payment/13/"
    headers = {
        "Authorization" : f"Bearer {token}"
    }

    get_response = requests.get( endpoint, headers=headers)
    print('satatus code=', get_response.json())








