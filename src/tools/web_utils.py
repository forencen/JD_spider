import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config.config import CONFIG
from utils import init_browser


def is_login(cookies):
    login_browser = init_browser(['--headless', 'log-level=2'])
    wait_login = WebDriverWait(login_browser, CONFIG['WAIT_TIME'])
    login_browser.get('https://jd.com')
    for cookie in cookies:
        if 'expiry' in cookie:
            cookie['expiry'] = int(cookie['expiry'])
        login_browser.add_cookie(cookie)
    login_browser.get('https://order.jd.com/center/list.action')
    time.sleep(2)
    _is_login = False
    try:
        wait_login.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            '#order01 > div > h3'))
        )
        _is_login = True
    except TimeoutException:
        _is_login = False
    login_browser.quit()
    return _is_login
