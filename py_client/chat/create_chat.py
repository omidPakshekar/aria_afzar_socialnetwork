import requests
endpoint = "http://127.0.0.1:8000/api/v1/accounts/login/"
psw = "omid1234"
data = {
    "email" : "omid@gmail.com",
    "password" : psw,
}

auth_response = requests.post( endpoint, data=data ) # HTTP request

if auth_response.status_code == 200:
    token = auth_response.json()['access_token']  
    endpoint = "http://127.0.0.1:8000/api/v1/chat/"
    headers = {
        "Authorization" : f"Bearer {token}"
    }
    data = {
        'friends' : {
                6,
                7
            
        }
    }
    get_response = requests.post(endpoint, headers=headers, data=data)
    print('status_code=', get_response.status_code)
    print('json=', get_response.json())

