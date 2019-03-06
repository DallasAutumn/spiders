import re
import time

from requests.exceptions import ConnectionError

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = Chrome()
wait = WebDriverWait(driver, 10)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'cookie': 'thw=cn; t=1a82c8acc029f28c0397341eeb9c303e; cna=g7JAFHo1pUICAdvv48VmWPj3; tracknick=%5Cu661F%5Cu5F71%5Cu5929%5Cu539Fnostalgia; tg=0; enc=eZKOhDtf95Zw3TXCxwWXst7nVEm2zEHSBY%2FHLwWSl44W7uowI5HhYDIcYTMC7qmjj25bIz5xnVijNTTBGNb7HA%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; miid=223014892010264765; v=0; cookie2=38c86626ee125c88da9b0e76d102ad07; _tb_token_=ebed8ee6e313e; unb=3440745235; sg=a58; _l_g_=Ug%3D%3D; skt=57609c511e89fa71; cookie1=AVGlPcB4ka7oPMoYvUAs2C5VQpQWf9Qe2eGGaoC%2FOGM%3D; csg=2f28e0ae; uc3=vt3=F8dByR1RnlR9keb393c%3D&id2=UNQz2E9PNbonQQ%3D%3D&nk2=s0%2FgKFCJuFUc%2B1CppdjHv9k%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D; existShop=MTU0NDExMTIxMQ%3D%3D; lgc=%5Cu661F%5Cu5F71%5Cu5929%5Cu539Fnostalgia; _cc_=URm48syIZQ%3D%3D; dnk=%5Cu661F%5Cu5F71%5Cu5929%5Cu539Fnostalgia; _nk_=%5Cu661F%5Cu5F71%5Cu5929%5Cu539Fnostalgia; cookie17=UNQz2E9PNbonQQ%3D%3D; uc1=cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&cookie21=VFC%2FuZ9ainBZ&cookie15=W5iHLLyFOGW7aA%3D%3D&existShop=false&pas=0&cookie14=UoTYMh97TDpCPw%3D%3D&lng=zh_CN; mt=ci=-1_1; isg=BEpKLVKlIoy0oamTLR82N-12mzDmKmeDpF1BUtSDTh0oh-tBvsgupUu1k_Nbd0Yt'

}


def search_food(url='https://www.taobao.com'):
    '''打开淘宝主页, 搜索美食索引页'''
    try:
        driver.get(url)
        input_ = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#q')))
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
        input_.send_keys('美食')
        submit.click()
        # 获取总页数
        total = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
        return total.text  # 返回总页数
    except ConnectionError:
        print('Your spider is defeated!')
    finally:
        time.sleep(3)
        driver.quit()


def main():
    total = int(re.compile('(\d+)').search(search_food()).group(1))
    print(total)


if __name__ == '__main__':
    main()
