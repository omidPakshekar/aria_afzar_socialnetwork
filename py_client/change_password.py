import requests


auth_endpoint = "http://127.0.0.1:8000/api/v1/token/"

data ={
    "email" : "mammad@gmail.com",
    "password" : "alib1234"
}

auth_response = requests.post(auth_endpoint, json=data)
print('auth_response=', auth_response.json())


endpoint = "http://127.0.0.1:8000/api/v1/accounts/change-password/"

if auth_response.status_code == 200:
    token = auth_response.json()['access']    
    data = {
        "current_password" : "alib1234",
        "new_password" : "omid1234",
    }
    headers = {
        "Authorization" : f"Bearer {token}"
    }
    get_response = requests.post( endpoint, headers=headers, json=data) # HTTP request
    print('data=', get_response.status_code)


