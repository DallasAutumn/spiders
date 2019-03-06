# selenium常用于自动化测试,在爬虫中主要解决JavaScript渲染问题

import time
import selenium as sel
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

driver = Chrome()
url = 'https://www.taobao.com'
driver.get(url)

time.sleep(2)
driver.close()
# try:
#     url = 'https://www.baidu.com'
#     driver.get(url)
#     input_ = driver.find_element_by_id('kw')
#     input_.send_keys('python')
#     input_.send_keys(Keys.ENTER)
#     wait = WebDriverWait(driver, 10)
#     wait.until(ec.presence_of_element_located((By.ID, 'content_left')))
#     print(driver.current_url)
#     print(driver.get_cookies)
#     print(driver.page_source)
# finally:
#     print('')
