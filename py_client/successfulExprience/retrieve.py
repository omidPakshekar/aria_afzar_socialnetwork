import requests


endpoint = "http://127.0.0.1:8000/api/v1/accounts/login/"
psw = "amir1234"
data = {
    "username" : "omid6",
    "email" : "omid6@gmail.com",
    "password" : psw,
}

auth_response = requests.post( endpoint, data=data )

endpoint = "http://localhost:8000/api/v1/exprience/"

if auth_response.status_code == 200:
    token = auth_response.json()['access_token']      
    headers = {
        "Authorization" : f"Bearer {token}"
    }
    data = {
        "title" : "Django development",
        "description" : "hi im django developer and im django developer and im django developer",        
    }
    data = {
        "title" : "javaaaaaaaaaaaaa",
    }
    get_response = requests.get( endpoint, headers=headers, data = data)

    print('status_code=', get_response.status_code)
    print('json=', get_response.json())
