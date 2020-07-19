"""
热点适用
"""
import datetime
import time

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import CONFIG
from task.base_task import BaseTask
from tools.logger_helper import logger
from tools.web_utils import init_browser


class HotTry(BaseTask):

    def __init__(self, cookies):
        super().__init__()
        self.set_cookies_to_browser(cookies)

    def task_handler(self, urls):
        for url in urls:
            try:
                logger.info('%s 开始申请' % url)
                self.browser.get(url)
                time.sleep(3)
                try_btn = self.find_element(
                    '#product-intro > div.info > div.try-info.clearfix.bigImg > div.info-detail.chosen > div > div.btn-wrap > a',
                    'css')
                if try_btn and '更多试用' not in try_btn.text:
                    try_btn.click()
                    time.sleep(2)
                    tip_select = 'body > div.ui-dialog.tipsAlert > div.ui-dialog-content > div > div.tip-tit'
                    try:
                        tip = self.find_element(tip_select, 'css')
                        if tip and '申请成功' in tip.text:
                            logger.info('%s 申请成功' % url)
                            continue
                    except NoSuchElementException as e:
                        pass
                    try:
                        css_select = 'body > div.ui-dialog > div.ui-dialog-content > div > div > div.btn > a.y'
                        self.wait_element(css_select,
                                          lambda: self.browser.find_element_by_css_selector(css_select).click() ,
                                          'css')
                        logger.info('%s 申请成功' % url)
                    except TimeoutException:
                        logger.info('%s 申请超时' % url)
                        continue
                else:
                    logger.info('%s 已经申请过' % url)
            except Exception:
                logger.error('%s 申请出错' % url, exc_info=True)
        logger.info('%s 已申请完毕' % datetime.date.today())

    def run(self):
        self.browser.get('https://try.jd.com/')
        hot_try = self.find_element('//*[@id="sliderBox"]')
        urls = [item.get_attribute("href") for item in hot_try.find_elements_by_xpath('./div[1]/ul/li//a[@href]')]
        self.task_handler(urls)






def click_jd_hot_try(cookies):
    browser = init_browser()
    wait_browser = WebDriverWait(browser, CONFIG['WAIT_TIME'])
    browser.get('https://jd.com')
    for cookie in cookies:
        if 'expiry' in cookie:
            cookie['expiry'] = int(cookie['expiry'])
        browser.add_cookie(cookie)
    browser.get('https://try.jd.com/')
    hot_try = browser.find_element_by_xpath('//*[@id="sliderBox"]')
    urls = [item.get_attribute("href") for item in hot_try.find_elements_by_xpath('./div[1]/ul/li//a[@href]')]

