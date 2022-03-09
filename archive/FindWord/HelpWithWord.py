

def GetParamsFromUser():
    Chars = input(
        'Введите доступные символы из которых должно состоять слово: ').replace(' ', '').lower()
    ListChars = []
    for Char in Chars:
        if Char not in ListChars:
            ListChars.append(Char)
        else:
            continue
    while True:
        try:
            CharNum = int(
                input('Введите количество символов в слове цифрой. Чтобы не ограничивать количество введите 0: '))
            if CharNum < 0:
                raise Exception('')
            break
        except Exception:
            print("Введите цифру!")
            continue
    KnowCharNum = input(
        'Введите номера известных символов цифрами, если есть через запятую: ').replace(' ', '')
    ListKnowChar = []
    KnowCharNum = KnowCharNum.split(',')
    for Num in KnowCharNum:
        if Num == '':
            break
        Char = input(
            "Введите символ под номером {} из слова: ".format(Num)).lower()
        CharDict = {Num: Char}
        ListKnowChar.append(CharDict)
    print('Итак. Ваше слово содердит буквы {}, в нем {} букв, мы знаем оттуда {} буквы.'.format(
        ', '.join(ListChars), str(CharNum), (','.join(KnowCharNum)
                                             )))
    Settings = ListChars, CharNum, ListKnowChar
    return Settings


def GetWord(Settings):
    ListChars = Settings[0]
    CharNum = Settings[1]
    ListKnowChar = Settings[2]
    with open('python\\FindWord\\DictWord', 'r', encoding='utf-8') as File:
        Words = File.read().lower().split('; ')
        for Word in Words:
            for Char in Word:
                if Char in ListChars:
                    FlagChar = True
                    continue
                FlagChar = False
                break
            if not FlagChar:
                continue
            if CharNum != 0 and len(Word) != CharNum:
                continue
            if ListKnowChar != []:
                FlagDict = False
                for Dict_ in ListKnowChar:
                    key = int(list(Dict_.keys())[0])
                    if len(Word) < key:
                        FlagDict = True
                        break
                    if Word[key-1] != Dict_[str(key)]:
                        FlagDict = True
                        break
            if FlagDict:
                continue

            print(Word)


def main():
    Settings = GetParamsFromUser()
    GetWord(Settings)


if __name__ == "__main__":
    main()
