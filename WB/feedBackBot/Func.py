"""
Описание функций и их использования
--Карточки товара в дальнейшем КТ
------------------------------------------------------------------------------------------------------------------------
RequestFeedback(string_1)
string_1 - переменная типа string, используется для указания токена аккаунта-продавца WB(wildberries), нужен, что бы
функция могла отправить запрос для получения отзывов
Возвращает отзывы в json формате, дополнительные параметры - не отвеченные, до 10 000 отзывов, пропускает первые 0 шт

Пример:
your_variable = RequestFeedback("token-string") #Получает неотвеченные отзывы
------------------------------------------------------------------------------------------------------------------------
WriteFeedbacks(response, stop_list)
respons - результат запроса из RequestFeedback()
stop_list - название или путь к файлу-стоп листу
Записывает отзывы в файл и разделяет для дальнейшей обработки
Вовращает количество отзывов в разных файлах(индекс 0 -5зв для автоответа, индекс 1 - стоп лист, 2 - остальные отзывы)
------------------------------------------------------------------------------------------------------------------------
LoadFeedback(category, index)
category - азвание категории в string (answer, stop_liust, other)
index  - номер в списке
Возвращает единичный экземпляр отзыва из масива отзыва, созданного с помощью WriteFeedbacks(), а так же
обратный индекс, показывающий сколько осталось ещ отзывов(-бесконечность... -100, -99, -98, -97... -1, 0)
------------------------------------------------------------------------------------------------------------------------
LocalFunc_Write
локальная функция для правильной записи WriteFeedbacks, регулирует, какие значения будут вписаны в файл для каждого
отзыва
------------------------------------------------------------------------------------------------------------------------
GenAnswer(excel_path_str, JSON_RequestFeedback)
excel_path_str - переменная типа string, используется для укзания пути к эксель файлу, с вариантами частей ответа,
функция использует первые 5 столбцов, игнорирет заголовки
JSON_RequestFeedback - переменная в json формате, используется для передачи информации об отзывах, полученных
через RequestFeedback(token)
Возвращает сгенерированный ответ на основе частей из предоставленного экселя, перемешивает случайным образом и
комбинирует

Пример:
your_variable = GenAnswer(pathToExcel, JSON_RequestFeedback)

Структура Эксель листа
Приветствие + спасибо за выбор  | Благодарность  |  Основной текст  |  Рекомендации  |  Прощание
            привет1             |     благ1      |        текст1    |       рек1     |    прощ1
            привет2             |     благ2      |        текст2    |       рек2     |    прощ2
            привет3             |     благ3      |        текст3    |       рек3     |    прощ3
            привет4             |     благ4      |        текст4    |       рек4     |    прощ4

Утрированый ответ:
комбинация из привет3 благ1 текст4 рек3 и подобное
------------------------------------------------------------------------------------------------------------------------
WriteAnswer(answer, feedback, WBAPIToken)
Отвечает на отзыв введёным текстом
answer - переменная ответа(в авто-ответе подставлять значение из GenAnswer
feedback - отзыв на который нужно ответить(подставлять значение из LoadFeedback()[0])
WBAPIToken - токен от вайлдберис аккаунта продавца - владельца КТ, на котором написан
этот отзыв
------------------------------------------------------------------------------------------------------------------------
Ошибки запросов на Wildberies API
Применимо  к RequestFeedback и WriteAnswer и др. функций, что используют токен

Код 200 - успешно
Код 400 - ошибка переданных параметров
Код 401 - отсутствие авторизации
Код 403 - ошибка авторизации(напр. не верный токен)
Код 404 - не найдено
Код 422 - дополнительные ошибки, когда запрос успешно отправлен и обработан, но результат не получен(например, когда
отсутствуют закончились/отзывы)

структура ошибки(json):
        {
        "data": null,                         #Дата - обычно пусто(null)
        "error": true,                        #Ошибка ли(булевая)
        "errorText": "Something went wrong",  #Текст ошибки
        "additionalErrors": null              #Дополнительные ошибки
        }
------------------------------------------------------------------------------------------------------------------------
Файл settings.ini обязательно должен быть прикреплен к проекту(расположение рядом с данным скриптом)
В нём укзан стоп лист слов и фраз для фильтрации автоответа, а так же в нем указывается токен

Пример структуры settings.ini файла на момент 29.05.2023:
# settings.ini
[MainSettings]
token = token_wb
stop_list = ["Слово1", "Слово2" ,"Слово3"]
------------------------------------------------------------------------------------------------------------------------
"""




import random
import requests
import pandas, openpyxl
import os, json, sys
import configparser


def RequestFeedback(WBAPIToken):
    header = {'Authorization': WBAPIToken}
    params = {'isAnswered': False, 'take': 5000, 'skip': 0}
    r = requests.get('https://feedbacks-api.wildberries.ru/api/v1/feedbacks', headers=header, params=params)  ##Сам запрос

    return r

def GenAnswer(responseDataExcel, value):
    excel = pandas.read_excel(responseDataExcel)
    InResp = str(excel.iloc[random.randint(0, excel.notna()[::-1].idxmax()[0]), 0])
    ThxResp = str(excel.iloc[random.randint(0, excel.notna()[::-1].idxmax()[1]), 1])
    MainResp = str(excel.iloc[random.randint(0, excel.notna()[::-1].idxmax()[2]), 2])
    RecResp = str(excel.iloc[random.randint(0, excel.notna()[::-1].idxmax()[3]), 3])
    BBResp = str(excel.iloc[random.randint(0, excel.notna()[::-1].idxmax()[4]), 4])
    Resp = str(InResp + ' ' + ThxResp + ' ' + MainResp + ' ' + RecResp + ' ' + BBResp)
    Resp = Resp.replace('{%Brand%}', value['Brand']).replace('{%Model%}', value['Product'])

    return Resp
def WriteFeedbacks(response, stop_list):
    try: open('answer', 'w').close()
    except: pass
    try: open('other', 'w').close()
    except: pass
    try: open('stop_list', 'w').close()
    except: pass
    answerLenght = stop_listLenght = otherLenght = 0
    for value in (response.json()['data']['feedbacks']):
        if (value['productValuation'] == 5):
            if any((match := substring.lower()) in value['text'].lower() for substring in stop_list):
                with open("stop_list", "a", encoding="utf-8") as myfile:
                    LocalFunc_Write(myfile, value)
            else:
                with open("answer", "a", encoding="utf-8") as myfile:
                    LocalFunc_Write(myfile, value)
        else:
            with open("other", "a", encoding="utf-8") as myfile:
                LocalFunc_Write(myfile, value)

    with open('answer',encoding="utf-8") as content:
        answerLenght = len(content.read().split("%/%")) - 1
    with open('stop_list',encoding="utf-8") as content:
        stop_listLenght = len(content.read().split("%/%")) - 1
    with open('other',encoding="utf-8") as content:
        otherLenght = len(content.read().split("%/%")) - 1

    return answerLenght,stop_listLenght,otherLenght

def LoadFeedback(category, index):
    with open(category,encoding="utf-8") as content:
        SplitedContent = content.read().split("%/%")
        if index <= len(SplitedContent) - 2:
            Feedback["id"] = SplitedContent[index].split('/id:/')[1].split('/Valuation:/')[0]
            Feedback["Valuation"] = SplitedContent[index].split('/Valuation:/')[1].split('/Text:/')[0]
            Feedback["Text"] = SplitedContent[index].split('/Text:/')[1].split('/Brand:/')[0]
            Feedback["Brand"] = SplitedContent[index].split('/Brand:/')[1].split('/Product:/')[0]
            Feedback["Product"] = SplitedContent[index].split('/Product:/')[1]
            return Feedback, (index - (len(SplitedContent) - 2))
        else:
            print('Error:CustomError' +'\n' +'The index is large and goes beyond the length of the array', file=sys.stderr)
            exit()

def WriteAnswer(answer, feedback, WBAPIToken):
    print(answer,'\n', feedback)
    header = {'Authorization': WBAPIToken}
    data = {"id": feedback['id'],
        "text": str(answer)}
    r = requests.patch(url='https://feedbacks-api.wildberries.ru/api/v1/feedbacks', headers=header, data=json.dumps(data))
    return r


Feedback = {'id': '', 'Valuation': '', 'Text': '', 'Brand': '', 'Product': ''}
FeedbackCount = {'answer': -1, 'other': -1, 'stop_list': -1}
def LocalFunc_Write(file, value):
    file.write('/id:/' + str(value['id']) +
                 '/Valuation:/' + str(value['productValuation']) +
                 '/Text:/' + value['text'] +
                 '/Brand:/' + value['productDetails']['brandName'] +
                 '/Product:/' + value['productDetails']['productName'] +'%/%')



def AutomaticWriteAnswer(WBAPIToken):
    r = RequestFeedback(WBAPIToken)
