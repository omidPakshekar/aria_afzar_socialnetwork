import requests
endpoint = "http://127.0.0.1:8000/api/v1/accounts/register/"
psw = "amir1234"
data = {
    "username" : "omid6",
    "email" : "omid6@gmail.com",
    "password1" : psw,
    "password2" : psw,
    "country" : "Iran",
    "year_of_birth" : "1996",
    "month_of_birth" : "september",
    "day_of_birth" : "24",
    "gender": "M",
}
get_response = requests.post( endpoint, json=data ) # HTTP request
print('json=', get_response.json())