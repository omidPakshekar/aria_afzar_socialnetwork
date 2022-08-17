import requests

auth_endpoint = "http://127.0.0.1:8000/api/v1/token/"

data ={
    "email" : "mammad@gmail.com",
    "password" : "omid1234"
}

auth_response = requests.post(auth_endpoint, json=data)
print('auth_response=', auth_response.json())


endpoint = "http://localhost:8000/api/v1/payment/payment/"

if auth_response.status_code == 200:
    token = auth_response.json()['access']    

    headers = {
        "Authorization" : f"Bearer {token}"
    }
    data = {
        "amount" : 6789,
        "payment_system" : "Bitcoin",        
    }
    get_response = requests.post( endpoint, headers=headers, json=data)

    print('status_code=', get_response.status_code)
    print('json=', get_response.json())
