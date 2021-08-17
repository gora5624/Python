from bs4 import BeautifulSoup
from my_lib import get_html


def ParsWordFromPage(url_in):
    html = get_html(url_in)
    soup = BeautifulSoup(html, 'lxml')
    ListWordTag = []
    ListWordTag = soup.find(
        'table', class_='table').find_all('td', class_='text-left')
    for WordTag in ListWordTag:
        Word = WordTag.find('a').text
        with open('python\\FindWord\\DictWord', 'a', encoding='utf-8') as Dict_:
            Dict_.write(Word + '; ')
            Dict_.close()


def ParsPagesUrl(MainUrl):
    html = get_html(MainUrl)
    soup = BeautifulSoup(html, 'lxml')
    ListCharPageTag = []
    ListCharPageUrl = []
    ListCharPageUrlWithPage = []
    ListCharPageTag = soup.find('div', class_='first-level').find_all(
        'a')
    # print(ListCharPageTag)
    for CharPageTag in ListCharPageTag:
        ChatUrl = MainUrl + CharPageTag.get('href')
        ListCharPageUrl.append(ChatUrl)
        # print(ListCharPageUrl)
    for CharPageUrl in ListCharPageUrl:
        html = get_html(CharPageUrl)
        soup = BeautifulSoup(html, 'lxml')
        try:
            Pagination = int(
                soup.find('ul', class_='pagination').find_all('a')[-1].text)
        except:
            Pagination = 1
        num = 1
        while num <= Pagination:
            Url = CharPageUrl[0:-1] + str(num)
            ListCharPageUrlWithPage.append(Url)
            num += 1
    return ListCharPageUrlWithPage


def main(MainUrl):
    ListUrlWithWord = ParsPagesUrl(MainUrl)
    for Url in ListUrlWithWord:
        ParsWordFromPage(Url)


MainUrl = 'https://ozhegov.slovaronline.com'
if __name__ == "__main__":
    main(MainUrl)
