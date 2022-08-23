import requests


endpoint = "http://localhost:8000/api/v1/payment/"
get_response = requests.get( endpoint)
# you must authenticate for retrive all object
# only admin can get all object
if get_response.status_code != "403":
    endpoint = "http://127.0.0.1:8000/api/v1/accounts/login/"
    psw = "amir1234"
    data = {
        "username" : "omid6",
        "email" : "omid6@gmail.com",
        "password" : psw,
    }

    auth_response = requests.post( endpoint, data=data ) # HTTP request
    # for get user inforamtion use username
    if auth_response.status_code == 200:
        token = auth_response.json()['access_token']  
        headers = {
            "Authorization" : f"Bearer {token}"
        }

        get_response = requests.get( endpoint, headers=headers)
        print('status code=', get_response.json())








