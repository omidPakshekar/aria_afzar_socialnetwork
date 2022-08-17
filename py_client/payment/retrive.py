import requests


endpoint = "http://localhost:8000/api/v1/payment/payment/1/"
get_response = requests.get( endpoint)
# you must authenticate for retrive
if get_response.status_code != "403":
    auth_endpoint = "http://127.0.0.1:8000/api/v1/token/"

    data ={
        "email" : "mammad@gmail.com",
        "password" : "omid1234"
    }

    auth_response = requests.post(auth_endpoint, json=data)
    endpoint = "http://localhost:8000/api/v1/payment/payment/13/"
    if auth_response.status_code == 200:
        token = auth_response.json()['access']    
        headers = {
            "Authorization" : f"Bearer {token}"
        }

        get_response = requests.get( endpoint, headers=headers)
        print('satatus code=', get_response.json())








