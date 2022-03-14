from uuid import uuid4
import requests 



url = 'https://suppliers-api.wildberries.ru/upload/file/multipart'
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImEyNjQwNTAzLTk0NjktNGFkYy04MzVhLWM5MTQzZWU0NDBkYiJ9.UCh5I_5bnet0S2JcV92oDWS3p8RgUP5dsOwglCYu6ZE'
fileID = str(uuid4())
data = {'Content-Disposition': 'form-data'}
headers = {'Authorization': '{}'.format(token), 
           'Content-Type': 'multipart/form-data;boundary=img',
           'X-File-Id':fileID}
files={'uploadfile': ('photo.jpg', open(r'F:\Done\69025844\photo\1.jpg', 'rb'), 'type=*/*')}
r = requests.post(url, headers=headers, files=files, data=data)
print(r.headers)
pass


