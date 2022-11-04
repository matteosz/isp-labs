import base64

encrypted = 'YWRtaW4sMTY2NzUxNDgzOCxjb200MDIsaHczLGV4MSx1c2Vy'

clear_text = base64.b64decode(encrypted)
print(clear_text)

new_text = str(clear_text).replace('user', 'admin')
print(new_text)

new_encrypted = base64.b64encode(new_text.encode())
print(new_encrypted.decode('utf-8'))