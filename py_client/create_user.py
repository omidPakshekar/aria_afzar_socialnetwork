import requests

endpoint = "http://127.0.0.1:8000/api/v1/accounts/register/"

data = {
    "username" : "mammad",
    "email" : "mammad@gmail.com",
    "password" : "mammad1234",
    "password2" : "mammad1234",
    "country" : "Iran",
    "year_of_birth" : "1997",
    "month_of_birth" : "september",
    "day_of_birth" : "24"
    
}
get_response = requests.post( endpoint, json=data ) # HTTP request
print('json=', get_response.json())


