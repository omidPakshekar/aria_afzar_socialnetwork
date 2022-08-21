import requests

endpoint = "http://127.0.0.1:8000/api/v1/accounts/register/"

data = {
    "username" : "mahan",
    "email" : "mahan.pak.est@gmail.com",
    "password" : "mahan1234",
    "password2" : "mahan1234",
    "country" : "Iran",
    "year_of_birth" : "1996",
    "month_of_birth" : "september",
    "day_of_birth" : "24"
    
}
get_response = requests.post( endpoint, json=data ) # HTTP request
print('json=', get_response.json())


