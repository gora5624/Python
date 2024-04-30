import pandas as pd
import requests
import time


token = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjMxMDI1djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTcxNzUyODk4NSwiaWQiOiJjZjViYzkwMi04MjI4LTQ5OWQtOTkzYS04N2QyYWQ5ZDk1ZTkiLCJpaWQiOjQ1MzIyOTIwLCJvaWQiOjUyNzczNiwicyI6MTI4LCJzaWQiOiJhYTQ3ZTQ4OS01OWUwLTQyMzItYTFiZi0wZTEyMzlmMDQyZjEiLCJ1aWQiOjQ1MzIyOTIwfQ.AAXFjklf63s4eErt3l6cKWecoUDAXMWz59haT23KPNzF35WNwlHML5i7a8NuIiOtZz-MXFjQ4hDS3jalRRfuEw'
headers = {'Authorization':'{}'.format(token)}
feedbacksList = []
for i in range(0,199990,5000):
    json = {
        'isAnswered': True,
        'take':5000,
        'skip':i
            }
    try:
        r = requests.get(url = r'https://feedbacks-api.wildberries.ru/api/v1/feedbacks', headers=headers, params=json)  
    except:
        continue
    if not len(r.json()['data']['feedbacks'])==0:
        feedbacksList.extend(r.json()['data']['feedbacks'])
        time.sleep(1)
    else:
        pd.DataFrame(feedbacksList).to_excel(r'd:\feedbacks.xlsx', index=False)