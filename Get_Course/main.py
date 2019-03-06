import re

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}


def get_html(page_url):
    response = requests.get(page_url, headers=headers)
    html = response.text
    return html


def parse(html):
    soup = BeautifulSoup(html, 'lxml')
    file_urls = soup.find_all('a', attrs={'target': '_blank', 'title': 'PDF'})
    return file_urls


def getPDF(file_url):
    response = requests.get(file_url, headers=headers)
    direc = r'D:\lovestudy\studybetter\微观经济学\课件'
    fn = direc + '\\' + file_url[-9:]
    with open(fn, 'wb') as f:
        f.write(response.content)


def main():
    page_url = r'http://course.buaa.edu.cn/portal/site/8e8d515e-40a5-477b-8ec2-f07845165b3e'
    html = get_html(page_url)
    print(parse(html))


if __name__ == '__main__':
    main()
