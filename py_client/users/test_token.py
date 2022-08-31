import requests
endpoint = "http://127.0.0.1:4444/api/v1/accounts/login/"
psw = "omid1234"
data = {
    "email" : "omid@gmail.com",
    "password" : psw,
}
endpoint = "http://127.0.0.1:4444/api/v1/accounts/refresh-token/"

# refresh_token= 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2MjAxODE2MSwiaWF0IjoxNjYxOTMxNzYxLCJqdGkiOiIxYTgwYjNkMjgwOWE0ZDhmYTZjNzk4NTdlOWViMDlmOSIsInVzZXJfaWQiOjF9.JUvD-jABYWYP0VYuRounZ4M3oSGyjDqWDNdxKTbmIfM'
# data = {
#     'refresh' : refresh_token
# }
# auth_response = requests.post( endpoint, data=data ) # HTTP request
# print(auth_response.json())
# token = auth_response.json()['access_token'] 
# print(token)
# token = auth_response.json()['refresh_token'] 
# print(token)

# print(auth_response.json())
access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjYxOTMyNzc1LCJpYXQiOjE2NjE5MzE3NjEsImp0aSI6ImVhMjA0YTMxZGYzYjQ1NzNhOGExNjU2OWVlMjNhYmQ1IiwidXNlcl9pZCI6MX0.s-2sM4RT18ihpRdeVkfzhGLaZQaEgzBE4CIF-JTquwk'
# refresh_token= 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2MjAxODE2MSwiaWF0IjoxNjYxOTMxNzYxLCJqdGkiOiIxYTgwYjNkMjgwOWE0ZDhmYTZjNzk4NTdlOWViMDlmOSIsInVzZXJfaWQiOjF9.JUvD-jABYWYP0VYuRounZ4M3oSGyjDqWDNdxKTbmIfM'
    
endpoint = "http://127.0.0.1:4444/api/v1/accounts/"

headers = {
    "Authorization" : f"Bearer {access_token}"
}
get_response = requests.get(endpoint, headers=headers)
print(get_response.json())
print(get_response.status_code)

 
