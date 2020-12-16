import re
from lxml import etree
from scrapy.http import HtmlResponse
from selenium import webdriver
from webdriver.common.by import by
from webdriver.support.ui import WebDriverWait
from webdriver.support import expected_conditions as EC

class seleniumMiddleware:

        def process_request(self, request)
                url = request.url
                if re.search(r'http://fundf10.eastmoney.com/jjjz_\d{6}.html', url):
                    options = webdriver.FirefoxOptions()
                    options.add_argument('--headless')
                    browser = webdriver.Firefox(firefox_options=options)
                    browser.get(url)
                    cur_source = browser.page_source
                    total_page = int(html.xpath(r'.//div[@class="pagebtns"]/label[last()-1]/text()')[0])
                    source = '1' + cur_source
                    while True:
                        try:
                            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(By.XPATH, r'.//div[@class="pagebtns"]/label[last()]'))
                            cur_source = browser.page_source
                            html = etree.HTML(cur_source)
                            cur_page = html.xpath(r'.//div[@class="pagebtns"]/label[@class="cur"]/text()')[0]
                            source = source + ' ' + cur_page + ' ' + cur_source
                            #
                            element.click()
                        finally:
                            browser.quit()
                            break
                    response = HtmlResponse(url=url, body=source, request=request, encoding='utf-8')    
                    return response

