import requests

auth_endpoint = "http://127.0.0.1:8000/api/v1/token/"

data ={
    "email" : "mammad@gmail.com",
    "password" : "mammad1234"
}

auth_response = requests.post(auth_endpoint, json=data)
print('auth_response=', auth_response.json())


endpoint = "http://localhost:8000/api/v1/exprience/1/add_comment/"

if auth_response.status_code == 200:
    token = auth_response.json()['access']    
    headers = {
        "Authorization" : f"Bearer {token}"
    }
    data = {
        "comment_text" : "it's good product"
    }

    get_response = requests.post(endpoint, headers=headers, data=data)

    print('status_code=', get_response.status_code)
    print('json=', get_response.json())
