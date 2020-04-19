import datetime
import logging
import time

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config.config import CONFIG
from utils import init_browser

log_file = '../log/try/logger_hot_try.log'
LOGGING_MSG_FORMAT = '[%(asctime)s] [%(levelname)s] [%(module)s] [%(funcName)s] [%(lineno)d] %(message)s'
LOGGING_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

logging.basicConfig(level=logging.INFO, filename=log_file, format=LOGGING_MSG_FORMAT, datefmt=LOGGING_DATE_FORMAT)
logger = logging.getLogger(__name__)


def click_jd_hot_try(cookies):
    browser = init_browser(options=['--headless', 'log-level=2'])
    wait_browser = WebDriverWait(browser, CONFIG['WAIT_TIME'])
    browser.get('https://jd.com')
    for cookie in cookies:
        if 'expiry' in cookie:
            cookie['expiry'] = int(cookie['expiry'])
        browser.add_cookie(cookie)
    browser.get('https://try.jd.com/')
    hot_try = browser.find_element_by_xpath('//*[@id="sliderBox"]')
    urls = [item.get_attribute("href") for item in hot_try.find_elements_by_xpath('./div[1]/ul/li//a[@href]')]
    for url in urls:
        try:
            time.sleep(3)
            logger.info('%s 开始申请' % url)
            browser.get(url)
            time.sleep(2)
            try_btn = browser.find_element_by_css_selector(
                '#product-intro > div.info > div.try-info.clearfix.bigImg > div.info-detail.chosen > div > div.btn-wrap > a')
            if try_btn and '更多试用' not in try_btn.text:
                try_btn.click()
                time.sleep(2)
                tip_select = 'body > div.ui-dialog.tipsAlert > div.ui-dialog-content > div > div.tip-tit'
                try:
                    tip = browser.find_element_by_css_selector(tip_select)
                    if tip and '申请成功' in tip.text:
                        logger.info('%s 申请成功' % url)
                        continue
                except NoSuchElementException as e:
                    pass
                try:
                    css_select = 'body > div.ui-dialog > div.ui-dialog-content > div > div > div.btn > a.y'
                    wait_browser.until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, css_select)
                        )
                    )
                    browser.find_element_by_css_selector(css_select).click()
                    logger.info('%s 申请成功' % url)
                except TimeoutException:
                    logger.info('%s 申请超时' % url)
                    continue
            else:
                logger.info('%s 已经申请过' % url)
        except Exception:
            logger.error('%s 申请出错' % url, exc_info=True)
    logger.info('%s 已申请完毕' % datetime.date())
