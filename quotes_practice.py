import re
import time
from multiprocessing.pool import Pool

import pymongo
import requests
from pyquery import PyQuery as pq

base_url = 'http://quotes.toscrape.com/'
max_index = 10

MONGO_HOST = 'localhost'
MONGO_DB = 'quotes'
MONGO_TABLE = 'main'

client = pymongo.MongoClient(host=MONGO_HOST)
db = client[MONGO_DB]


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        print('processing time is', end_time-start_time)
    return wrapper


def get_html(url=base_url):
    try:
        response = requests.get(url)
        # print(response.text)
        html = response.text
        return html
    except ConnectionError:
        print('Error!')
        return None


def parse(html):
    doc = pq(html)
    items = doc('.quote').items()
    # for item in items:
    #     yield{
    #         'text': item.find('.text').text(),
    #         'author': item.find('.author').text()
    #     }
    for item in items:
        yield{
            'text': item.find('.text').text(),
            'author': item.find('.author').text()
        }


def save_to_mongo(data):
    db[MONGO_TABLE].insert(data)


def main(page_index):
    url = base_url + '/page/' + str(page_index) + '/'
    html = get_html(url)
    data = parse(html)
    # for each in data:
    #     print(each)
    for each in data:
        save_to_mongo(each)


if __name__ == '__main__':
    with Pool() as pool:
        pool.map(main, [i for i in range(1, max_index+1)])
