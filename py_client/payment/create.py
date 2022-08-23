import requests
endpoint = "http://127.0.0.1:8000/api/v1/accounts/login/"
psw = "amir1234"
data = {
    "username" : "omid6",
    "email" : "omid6@gmail.com",
    "password" : psw,
}

auth_response = requests.post( endpoint, data=data ) # HTTP request
# for get user inforamtion use username
endpoint = "http://localhost:8000/api/v1/payment/"
if auth_response.status_code == 200:
    token = auth_response.json()['access_token']   
    headers = {
        "Authorization" : f"Bearer {token}"
    }
    data = {
        "amount" : 3.56,
        "payment_system" : "Bitcoin",        
    }
    get_response = requests.post( endpoint, headers=headers, json=data)

    print('status_code=', get_response.status_code)
    print('json=', get_response.json())
