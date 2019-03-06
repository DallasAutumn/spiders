import requests
from pyquery import PyQuery as pq


base_url = "https://movie.douban.com/subject/26266893/comments?start={}&limit=20&sort=new_score&status=P"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36"}


def fetch(url):
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        return html
    return None


def parse(html):
