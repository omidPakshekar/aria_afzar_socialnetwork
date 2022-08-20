import requests

auth_endpoint = "http://127.0.0.1:8000/api/v1/token/"

data ={
    "email" : "mammad@gmail.com",
    "password" : "mammad1234"
}

auth_response = requests.post(auth_endpoint, json=data)
print('auth_response=', auth_response.json())


endpoint = "http://localhost:8000/api/v1/post/1/like/"

if auth_response.status_code == 200:
    token = auth_response.json()['access']    
    headers = {
        "Authorization" : f"Bearer {token}"
    }

    get_response = requests.put( endpoint, headers=headers)

    print('status_code=', get_response.status_code)
    print('json=', get_response.json())
