from datetime import datetime, timedelta, timezone
from numpy import int64, int8
# import multiprocessing
import requests
from ftfy import fix_text
import json
import pandas as pd
# from PyQt6.QtCore import QThreadPool, QRunnable
from threading import Thread #, Event
# from multiprocessing import Process
from os.path import join as joinPath
# from copy import deepcopy
# from memory_profiler import profile
import gc

class OrdersGetter():
    def __init__(self, seller, ordersFilePath, allInOne, putNom, rawData, saveSKU, consolid) -> None:
        self.urlGetOrders = 'https://suppliers-api.wildberries.ru/api/v3/orders'
        self.pathTo1CNom = r'\\192.168.0.33\shared\_Общие документы_\Егор\ШК\ШК.txt'
        self.ordersFilePath = ordersFilePath
        self.seller = seller
        self.putNomFlag = putNom
        self.allInOneFlag = allInOne
        self.rawDataFlag = rawData
        self.saveSKUFlag = saveSKU
        self.consolidFlag = consolid
        self.orders = []


    def getOrders(self, token: str, date_from: datetime, date_to: datetime):
        try:
            self.getOrdersProc(token, date_from, date_to)
        except:
            if not self.orders:
                return self.orders
            else:
                return None
        if len(self.orders) != 0:
            if self.putNomFlag:
                self.processingOrders()
            else:
                self.orders = pd.DataFrame(self.orders)
                self.orders['Продавец'] = self.seller
            if not self.allInOneFlag:
                self.saveOrders()

    def processingOrders(self):
        dataForm1C = pd.DataFrame(pd.read_table(self.pathTo1CNom, sep='\t', dtype=str))
        ordersProcessed = []
        for line in self.orders:
            for sku in line['skus']:
                line.update({'sku': sku})
                line.update({'Артикул WB': line['nmId']})
                line.update({'Дата': datetime.strptime(line['createdAt'].split('T')[0], '%Y-%m-%d').date().strftime('%d.%m.%Y')})
                line.update({'Время': datetime.strptime(line['createdAt'].split('T')[1], '%H:%M:%SZ').time().strftime('%H:%M:%S')})
                line.update({'Количество': 1})
                line.update({'Цена': line['convertedPrice']/100})
                line.update({'Продавец': self.seller})
                ordersProcessed.append(line)
        self.orders = ordersProcessed
        dfOrders = pd.DataFrame(self.orders)
        dfOrders['sku'] = dfOrders['sku'].astype(str)
        # dataForm1C['Штрихкод'] = dataForm1C['Штрихкод'].astype(str)
        dataTMP = pd.merge(dfOrders, dataForm1C, left_on='sku', right_on='Штрихкод', how='left')
        dataTMP['Продавец'] = self.seller
        #  столбцы "номенклатура" и "штришкод" из dataTMP в self.orders
        # dataTMP.drop(['sku'], axis=1, inplace=True)
        if not self.rawDataFlag:
            self.orders = dataTMP.loc[:, ['Штрихкод', 'Артикул WB' ,'Номенклатура', "Дата", "Время", "Количество", "Цена", "Продавец"]]
            self.orders.fillna(0, inplace=True)
            self.orders['Штрихкод'] = self.orders['Штрихкод'].astype(int64)
            if not self.saveSKUFlag:
                self.orders = self.orders.drop(['Штрихкод'] , axis=1)
                self.orders
        else:
            self.orders = dataTMP
        # сложить строки в dataTMP по полю "Количество"
        if self.consolidFlag:
            self.orders = self.orders.groupby(['Номенклатура'])['Количество'].sum().reset_index()


    def saveOrders(self):
        #df = pd.DataFrame(self.orders)
        # добавить в dataFrame df новый столбец с названием Продавец и значение self.seller
        #df['Продавец'] = self.seller
        # Если в файле более милиона строк то сохраняем в csv, если меньше то в xlsx:
        date = datetime.now().date().strftime('%d.%m.%Y')
        if self.orders.shape[0] > 1000000:
            self.orders.to_csv(joinPath(self.ordersFilePath, f'{self.seller} от {date}.csv'), index=False, sep='\t')
        else:
            self.orders.to_excel(joinPath(self.ordersFilePath, f'{self.seller} от {date}.xlsx'), index=False)

    def getOrdersProc(self, token: str, date_from: datetime, date_to: datetime):
        headers = {
            'Authorization': token,
        }
        page = 0
        time = datetime.min.time().replace(tzinfo=timezone.utc)
        date_from = datetime.combine(date_from, time)
        date_to = datetime.combine(date_to, time)
        params = {'limit': 1000,
                  'next': page,
                  'dateFrom': int(date_from.timestamp()),
                  'dateTo':int(date_to.timestamp())}
        countTry = 0
        while countTry<10:
            try:
                response = requests.get(self.urlGetOrders, headers=headers, params=params, timeout=50)
            except requests.exceptions.ConnectionError:
                countTry += 1
                continue
            except requests.exceptions.ReadTimeout:
                countTry += 1
                continue
            if response.status_code != 200:
                if countTry > 10:
                    raise Exception(f'Ошибка получения заказов: {response.status_code}\n {response.text}')
                countTry += 1
                continue
            fixed_text = fix_text(response.text)
            data = json.loads(fixed_text)
            self.orders.extend(data['orders'])
            if 'next' not in data:
                break
            params['next'] = data['next']
            countTry = 0
        return 



class WorkerQueue(Thread):
    def __init__(self, AnyFunction, **kwargs) -> None:
        super().__init__()
        self.AnyFunction = AnyFunction
        self.kwargs = kwargs

        
    def run(self):
        self.AnyFunction(**self.kwargs)

