import requests
from tampering_cookies import tamper_cookie

# Client trying to tamper cookies

username, password = 'matt', 'pass'

session = requests.session()

cookie_name = 'LoginCookie'

session.post("http://127.0.0.1:5000/login",
                data={"username": username,"password": password})

print(session.cookies[cookie_name])
tampered = tamper_cookie(session.cookies[cookie_name])

response = session.get("http://127.0.0.1:5000/")
print(response)

session.cookies[cookie_name] = None
session.cookies.set(cookie_name, tampered, domain='localhost', path='/')

response = session.get("http://127.0.0.1:5000/")
print(response)