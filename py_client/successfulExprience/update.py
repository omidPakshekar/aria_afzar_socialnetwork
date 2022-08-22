import requests


endpoint = "http://127.0.0.1:8000/api/v1/accounts/login/"
psw = "amir1234"
data = {
    "email" : "omid6@gmail.com",
    "password" : psw,
}

auth_response = requests.post( endpoint, data=data )

endpoint = "http://localhost:8000/api/v1/exprience/1/"

if auth_response.status_code == 200:
    token = auth_response.json()['access_token']
    headers = {
        "Authorization" : f"Bearer {token}"
    }
    data = {
        'admin_check': False
    }
    get_response = requests.patch(endpoint, headers=headers, data=data)

    print('status_code=', get_response.status_code)
    print('json=', get_response.json())    