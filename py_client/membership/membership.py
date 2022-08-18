import requests

"""  membership
    "http://localhost:8000/api/v1/accounts/membership/"  
    "403" --> authentication problem
    post --> create --> status_code = 302 already exist
                    --> status_code = 201 created
                    --> status_code = 400 bad input
    get  ---> 302 found
         ---> 404 not found --> output = user dosent have permission
""" 

data = {
    'month' : '1',
}

endpoint = "http://localhost:8000/api/v1/accounts/membership/"
get_response = requests.post( endpoint, data=data)
# you must authenticate for retrive all object
# only admin can get all object
if get_response.status_code != "403":
    auth_endpoint = "http://127.0.0.1:8000/api/v1/token/"

    data ={
        "email" : "omid@gmail.com",
        "password" : "omid1234"
    }

    auth_response = requests.post(auth_endpoint, json=data)
    if auth_response.status_code == 200:
        token = auth_response.json()['access']    
        headers = {
            "Authorization" : f"Bearer {token}"
        }
        data = {
            'month' : '1',
        }
        get_response = requests.get(endpoint, headers=headers)
        print('detail=', get_response.json())
        print('status code=', get_response.status_code)




