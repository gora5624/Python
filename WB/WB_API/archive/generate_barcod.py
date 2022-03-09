import requests
import json
from my_lib import write_csv


def generate_bar_WB():
  url = "https://suppliers-api.wildberries.ru/card/getBarcodes"
  headers = {'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjgyYTU2OGZlLTgyNTctNGQ2Yi05ZTg1LTJkYTgxMTgxYWI3MSJ9.ROCdF7eOfTZA-atpsLGTAi15yDzHk2UMes05vwjZwn4',
            'Content-Type': 'application/json',
            'accept': 'application/json'}
  data = "{\"id\":1,\"jsonrpc\":\"2.0\",\"params\":{\"quantity\":1,\"supplierID\":\"3fa85f64-5717-4562-b3fc-2c963f66afa6\"}}"

  r = requests.post(url, data=data, headers=headers)
  data_from_wb = r.json()
  return data_from_wb['result']['barcodes'][0])
