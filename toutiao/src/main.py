import json
import os
import re
from urllib.parse import urlencode

import pymongo
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

direc = os.path.dirname(__file__)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}


def get_index_page(offset, kw):
    info = {
        'offset': offset,
        'format': 'json',
        'keyword': kw,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 1,
        'from': 'search_tab'
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(info)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_index_page(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')


def get_detail_page(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求详情页出错', url)
        return None


def parse_detail_page(html):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('title')[0].get_text()
    images_pattern = re.compile('var gallery = (.*?);', re.S)
    result = re.search(images_pattern, html)
    if result:
        print(result.group(1))


def main():
    html = get_index_page(0, '街拍')
    for url in parse_index_page(html):
        html = get_detail_page(url)
        if html:
            parse_detail_page(html)


if __name__ == '__main__':
    main()
