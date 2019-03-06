import json
import os
import re
from multiprocessing.pool import Pool

import pandas as pd
import pymongo
import requests
from requests.exceptions import RequestException

from config import *

direc = os.path.dirname(__file__)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

def get_one_page(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    '''用正则表达式获取序号, 名称, 上映时间'''

    pattern = re.compile(
        '<dd>.*?board-index-.*?>(\d+)</i>.*?<a href.*?title="(.*?)".*?</a>.*?"releasetime">(.*?)</p>.*?</dd>', re.S)
    items = re.findall(pattern=pattern, string=html)
    for item in items:
        yield{
            'index': item[0],
            'title': item[1],
            'releasetime': item[2][5:]}


# def to_file(content):
#     fp = direc + r'\result.txt'
#     with open(fp, 'a', encoding='utf-8') as f:
#         f.write(json.dumps(content, ensure_ascii=False) + '\n')
def save_to_mongo(result):
    db[MONGO_TABLE].insert(result)

def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    result = parse_one_page(html)
    # f = open(file=direc+r'result.xlsx', mode='a')
    # for data in result:
    #     se = pd.Series(data=data)
    #     se.to_excel(excel_writer=f)
    # f.close()
    save_to_mongo(result)

if __name__ == '__main__':
    #构造0到90的数组, 遍历每一个页面, 放到进程池中实现秒抓
    pool = Pool()
    pool.map(main, [i*10 for i in range(10)])
