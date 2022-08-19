import requests

auth_endpoint = "http://127.0.0.1:8000/api/v1/token/"

data ={
    "email" : "amir@gmail.com",
    "password" : "amir1234"
}

auth_response = requests.post(auth_endpoint, json=data)
print('auth_response=', auth_response.json())


endpoint = "http://localhost:8000/api/v1/exprience/1/"

if auth_response.status_code == 200:
    token = auth_response.json()['access']    
    headers = {
        "Authorization" : f"Bearer {token}"
    }
    data = {
        "title" : "Django development",
        "description" : "hi im django developer and im django developer and im django developer",        
    }
    get_response = requests.get( endpoint, headers=headers)

    print('status_code=', get_response.status_code)
    print('json=', get_response.json())
