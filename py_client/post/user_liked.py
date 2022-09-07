import requests
endpoint = "http://127.0.0.1:8000/api/v1/accounts/login/"
psw = "amir1234"
data = {
    "email" : "omid5@gmail.com",
    "password" : psw,
}

auth_response = requests.post( endpoint, data=data ) # HTTP request

if auth_response.status_code == 200:
    token = auth_response.json()['access_token']     
    headers = {
        "Authorization" : f"Bearer {token}"
    }
    endpoint = "http://localhost:8000/api/v1/post/1/like/"

    get_response = requests.put( endpoint, headers=headers)

    print('status_code=', get_response.status_code)
    print('json=', get_response.json())
