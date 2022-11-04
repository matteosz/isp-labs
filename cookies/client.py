import requests

username, password = 'matt', 'pass'

session = requests.session()

session.post("http://127.0.0.1:5000/login",
                data={"username": username,"password": password})

print(session.cookies)

session.get("http://127.0.0.1:5000/")

session.cookies.update({"username": 'admin',"password": '42'})

print(session.cookies)

session.get("http://127.0.0.1:5000/")