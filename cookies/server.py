from flask import Flask, make_response, request
import time
import hmac
from hashlib import sha1
import base64
import random
import string

random.seed = 100

def random_string(length):
    result_str = ''.join(random.choice(string.ascii_letters) for _ in range(length))
    return result_str

app = Flask(__name__)

cookie_name = "LoginCookie"
private_key = random_string(8).encode()
admin_user, admin_password = 'admin', '42'

def create_cookie(username, password):
    timestamp, domain, hw, ex = str(int(time.time())), "com402", "hw3", "ex2"

    if username == admin_user and password == admin_password:
        role = "admin"
    else:
        role = "user"

    cookie = ",".join([username,timestamp,domain,hw,ex,role])
    signature = hmac.new(private_key, cookie.encode(), sha1)
    cookie += "," + signature.hexdigest()
   
    return base64.b64encode(cookie.encode()).decode('utf-8')

def validate_cookie(cookie):
    try:
        decoded = base64.b64decode(cookie.encode()).decode("utf-8")
    except:
        return False
    
    base_cookie, cookie_hmac = decoded.rsplit(",", 1)
    
    original_hmac = hmac.new(private_key, base_cookie.encode(), sha1).hexdigest()

    return cookie_hmac == original_hmac

@app.route("/login",methods=['POST'])
def login():
    
    username = request.form.get('username')
    password = request.form.get("password")
    
    if username == None or username == '' or password == None or password == '':
        return

    cookie = create_cookie(username, password)
    response = make_response("Logged in")
    response.set_cookie(cookie_name, cookie)
   
    return response

@app.route("/auth",methods=['GET'])
def auth():
    cookie = request.cookies.get(cookie_name)
    if cookie is None or validate_cookie(cookie) is False:
        return "Tampered cookie", 403
    
    decoded = base64.b64decode(cookie.encode()).decode("utf-8")
    role = decoded.split(",")[5]
    
    if role == "admin":
        return "Admin", 200
        
    return "User", 201

if __name__ == '__main__':
    app.run()