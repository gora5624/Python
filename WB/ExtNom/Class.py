import pandas as pd
import requests


class UploadTMPImage():
    def __init__(self) -> None:
        self.url = 'https://suppliers-api.wildberries.ru/content/v1/media/save'
        self.urlImage = 'http://95.78.233.163:8001/wp-content/uploads/1.jpg'
        self.pathToListNom = r'"F:\Downloads\report_2023_11_8 (1).xlsx"'
        self.headersReq = {'Authorization': '{}'.format(token)}


    def updateNom(self, sellerArt):
        jsonRequest = {
            "vendorCode": sellerArt,
            #"data": line['Медиафайлы'].split(';')
            "data": [self.urlImage]
            }
        r = requests.post(url=self.url, json=jsonRequest, headers=self.headersReq)
    

    def getSellerArtList(self):
        df = pd.DataFrame(pd.read_excel(self.pathToListNom))
        return df['Артикул продавца'].values.tolist()


    def uploadsNom(self):
        for sellerArt in self.getSellerArtList():
            self.updateNom(sellerArt)
    