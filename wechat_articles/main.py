# kw::query, type, page
from multiprocessing.pool import Pool
from urllib.parse import urlencode

import pymongo
import requests
from lxml.etree import XMLSyntaxError
from pyquery import PyQuery as pq
from requests.exceptions import ConnectionError

from config import *

client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DB]

headers = {
    'Cookie': 'CXID=DB7DC87A13F828356185FFDBDB2A2C71; SUID=3FEDCF3C5B68860A5BBF479A000E00EB; weixinIndexVisited=1; SUV=00134F726A272A3F5BCF0B3A5733A543; UM_distinctid=1670322e39114c-0d11bee5d5a59-4313362-1fa400-1670322e392419; SMYUV=1541946094541250; ld=cyllllllll2bfyLwlllllVsHGtDlllll5G@H2lllll9lllllRZlll5@@@@@@@@@@; ad=GwfD9lllll2bs1WzlllllVZpjFwlllll5G@H5Zllll9lllllx4Dll5@@@@@@@@@@; wapsogou_qq_nickname=; ABTEST=1|1544022831|v1; SUIR=05101D513A3E408A3776B2D23B361474; PHPSESSID=p9gj076s6eba5veb1p5skif325; seccodeErrorCount=7|Wed, 05 Dec 2018 15:29:32 GMT; sct=6; SNUID=1635C3A93B3940743E75851A3CE49732; JSESSIONID=aaa-COiHX2eR2btQlE6Cw; IPLOC=US',
    'Host': 'weixin.sogou.com',
    'Referer': 'https://open.weixin.qq.com/connect/qrconnect?appid=wx6634d697e8cc0a29&scope=snsapi_login&response_type=code&redirect_uri=https%3A%2F%2Faccount.sogou.com%2Fconnect%2Fcallback%2Fweixin&state=e7e633bf-d3ef-49ff-9dd5-d25eb2db8b84&href=https%3A%2F%2Fdlweb.sogoucdn.com%2Fweixin%2Fcss%2Fweixin_join.min.css%3Fv%3D20170315',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'}


proxy = None
max_count = 5


def get_index(kw, page, req_type=2, base_url='https://weixin.sogou.com/weixin?'
              ):
    query_para = {
        'query': kw,
        'page': page,
        'type': req_type,  # request for an article
    }
    queries = urlencode(query_para)
    url = base_url + queries
    html = get_html(url)
    return html


def get_html(url=None, count=1):
    global proxy
    print('Now crawling:', url, 'for the', count, 'time')

    if count >= max_count:
        print('Tried too many times!')
        return None
    try:
        if proxy:
            proxies = {'http': 'http://' + proxy}
            # reject redirection in order to get status code correctly.
            response = requests.get(
                url, allow_redirects=False, headers=headers, proxies=proxies)
        else:
            response = requests.get(
                url, allow_redirects=False, headers=headers)
        if response.status_code == 200:
            html = response.text
            return html
        if response.status_code == 302:
            # Need proxy
            print('302')
            proxy = get_proxy()
            if proxy:
                print('Now Using Proxy', proxy)
                return get_html(url)
            else:
                print('Get proxy failed!')
                return None
    except ConnectionError as CE:
        print('ConnectionError Occured', CE.args)
        count += 1
        proxy = get_proxy()
        return get_html(url)  # if failed, retry
    finally:
        pass
# print(get_index('北航街舞社', 1))


def get_proxy(proxy_pool_url='http://localhost:5555/random'
              ):
    try:
        response = requests.get(proxy_pool_url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


def parse_index(html):
    doc = pq(html)
    items = doc('.news-box .news-list li .txt-box h3 a').items()
    for item in items:
        yield item.attr('href')


def get_detail(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.text
        return None
    except ConnectionError:
        return None


def parse_detail(html):
    doc = pq(html)

    title = doc('.rich_media_title').text()
    content = doc('.rich_media_content').text()
    date = doc('#publish_time').text()
    nickname = doc('#js_profile_qrcode > div > strong').text()
    wechat = doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()

    return{
        'title': title,
        'date': date,
        'content': content,
        'nickname': nickname,
        'wechat': wechat
    }


def save_to_mongo(data):
    try:
        if db[MONGO_COLLECTION].update({'title': data['title']}, {'$set': data}, True):
            print('Saved to mongo', data['title'])
            return 170812
        else:
            print('Failed to save', data['title'])
            return 177717
    except XMLSyntaxError:
        return None


def main(total_page):
    for page in range(1, total_page+1):
        html = get_index('python', page)
        # print(html)
        if html:
            article_urls = parse_index(html)
            for article_url in article_urls:
                article_html = get_detail(article_url)
                if article_html:
                    article_data = parse_detail(article_html)
                    if article_data:
                        print(article_data)
                        save_to_mongo(article_data)


if __name__ == '__main__':
    # with Pool() as pool:
    #     pool.map(main, [i*10 for i in range(1, 10)])
    main(101)
