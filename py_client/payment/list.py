import requests


endpoint = "http://localhost:8000/api/v1/payment/"
get_response = requests.get( endpoint)
# you must authenticate for retrive all object
# only admin can get all object
if get_response.status_code != "403":
    auth_endpoint = "http://127.0.0.1:8000/api/v1/token/"

    data ={
        "email" : "omid@gmail.com",
        "password" : ""
    }

    auth_response = requests.post(auth_endpoint, json=data)
    endpoint = "http://localhost:8000/api/v1/payment/"
    if auth_response.status_code == 200:
        token = auth_response.json()['access']    
        headers = {
            "Authorization" : f"Bearer {token}"
        }

        get_response = requests.get( endpoint, headers=headers)
        print('status code=', get_response.json())







