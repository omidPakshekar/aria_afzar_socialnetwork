import requests
endpoint = "http://127.0.0.1:4444/api/v1/accounts/login/"
psw = "omid1234"
data = {
    "email" : "omid@gmail.com",
    "password" : psw,
}

auth_response = requests.post( endpoint, data=data ) # HTTP request

if auth_response.status_code == 200:
    token = auth_response.json()['access_token']  
    endpoint = "http://127.0.0.1:4444/api/v1/accounts/omid5/accept-profile-pic/"
    headers = {
        "Authorization" : f"Bearer {token}"
    }
    data = {
        "username" : 'omid5'
    }
    get_response = requests.post(endpoint, headers=headers)
    print('status_code=', get_response.status_code)
    print('json=', get_response.json())


