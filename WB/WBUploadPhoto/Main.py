from uuid import uuid4
import requests 



url = 'https://suppliers-api.wildberries.ru/upload/file/multipart'
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjEyODkyYmRkLTEwMTgtNDJhNi1hYzExLTExODExYjVhYjg4MiJ9.nJ82nhs9BY4YehzZcO5ynxB0QKI-XmHj16MBQlc2X3w'
fileID = str(uuid4())
data = {'Content-Disposition': 'form-data; name=uploadfile; filename=photo.jpg'}
headers = {'Authorization': '{}'.format(token), 
           'X-File-Id':fileID,
           'Content-Type': 'multipart/form-data;boundary=img',
           'Content-Disposition': 'form-data; name=uploadfile; filename=photo.jpg'}
with open(r'F:\Done\69052696\photo\1.jpg', 'rb') as file:
    a = file.read()
files={'uploadfile': ('photo.jpg', a, 'type=image/jpeg')}
r = requests.post(url, headers=headers, files=files)
print(r.headers)
pass


