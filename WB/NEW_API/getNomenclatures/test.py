import requests

jsonRequestsGetCardFirst = {
  "sort": {
    "cursor": {
      "nmID": 88562511,
      'limit':1000
    },
    "filter": {
      "withPhoto": -1
    },
    "sort": {
      "sortColumn": "updateAt",
      "ascending": False
    }
  }
}
headersGetCard = {'Authorization': '{}'.format('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjM3ZGIyZjExLTYyMmYtNDhkNC05YmVhLTE3NWUxNDRlZWVlNSJ9.yMAeIv0WWmF3rot06aPraiQYDOy522s5IYnuZILfN6Y')}
responce = requests.post('https://suppliers-api.wildberries.ru/content/v1/cards/cursor/list', json=jsonRequestsGetCardFirst, headers=headersGetCard)

a = responce.json()
a