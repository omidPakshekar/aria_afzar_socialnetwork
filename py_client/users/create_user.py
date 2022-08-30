import requests
endpoint = "http://omidpak.pythonanywhere.com/api/v1/accounts/register/"
psw = "amir12304"
data = {
    "username" : "omidpafdk2",
    "email" : "omid.pakshekar1378@gmail.com",
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