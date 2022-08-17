import requests

auth_endpoint = "http://127.0.0.1:8000/api/v1/token/"

data ={
    "email" : "omid@gmail.com",
    "password" : "est14641"
}

auth_response = requests.post(auth_endpoint, json=data)
print('auth_response=', auth_response.json())


endpoint = "http://localhost:8000/api/v1/payment/15/change-status/"

if auth_response.status_code == 200:
    token = auth_response.json()['access']    
    headers = {
        "Authorization" : f"Bearer {token}"
    }
    data = {
        "status" : "Accept",
        "description" : "admin accept this request",        
    }
    get_response = requests.put(endpoint, headers=headers, json=data)

    print('status_code=', get_response.status_code)
    print('json=', get_response.json())
