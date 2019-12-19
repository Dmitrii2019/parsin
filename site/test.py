import csv
import requests
# import pyinstaller
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
url_ = input('Введите название сайта linoleum-sklad.ru: ') #linoleum-sklad.ru
type_ = input('Введите тип покрытия linoleum: ')
base_url = f'https://{url_}/{type_}?limit=2000' #'https://linoleum-sklad.ru/linoleum?limit=2000'


def session_get(base_url, headers):
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        print('Ответ сервера 200')
    else:
        print('Не удалось подключится')
    return request


def parser_site():
    request = session_get(base_url, headers)
    jobs = []
    soup = bs(request.content, 'html.parser')
    divs = soup.find_all('div', attrs={'class': 'info'})
    for div in divs:
        title = div.find('a', attrs={'class': 'name'}).text
        prices = div.find('span', attrs={'class': 'price'}).text
        jobs.append({
            'title': title,
            'prices': prices.split()
        })
    return jobs


def files_writer(jobs):
    file_name = input('Имя файла для сохранения: ')
    with open(f'{file_name}.csv', 'w', encoding='utf-8') as f:
        a_pen = csv.writer(f)
        a_pen.writerow(('название', 'цена'))
        for job in jobs:
            a_pen.writerow((job['title'], job['prices']))
    print('Файл создан')


print('PARSER.DA')
password = input('Пароль: ')
hooves = 1
while password != '555':
    if hooves != 3:
        print('Не верный пароль')
        password = input('Пароль: ')
        hooves += 1
    else:
        print('В доступе отказано')
        break
else:
    print('Вход в программу')
    jobs = parser_site()
    files_writer(jobs)



