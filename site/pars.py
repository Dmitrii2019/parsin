import csv
import requests
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

base_url = 'https://linoleum-sklad.ru/linoleum?limit=20000'


def parser_site(base_url, headers):
    jobs = []
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        request = session.get(base_url, headers=headers)  #
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
    with open('par_Lin.csv', 'w') as f:
        a_pen = csv.writer(f)
        a_pen.writerow(('название', 'цена'))
        for job in jobs:
            a_pen.writerow((job['title'], job['prices']))


jobs = parser_site(base_url, headers)
files_writer(jobs)
