import os
import json
import time
import sys

from selenium import webdriver


def get_cookies(key=None):
    if os.path.exists('../resources/cookies.json'):
        with open('../resources/cookies.json', mode='r', encoding='utf-8') as f:
            res = json.load(f)
            ts = int(time.time())
            main_expiry = min([item.get('expiry', 999999999999999) for item in res])
            if main_expiry < ts:
                return None

            if key:
                v = [item.get('value') for item in res if item.get('name') == key]
                return v[0] if v else None
            else:
                return res
    else:
        return None


def write_cookies(cookies):
    with open('../resources/cookies.json', mode='w', encoding='utf-8') as f:
        json.dump(cookies, f)


def init_browser(options=None):
    # 打开无界面的chrome浏览器
    if options is None:
        options = []
    chrome_options = webdriver.ChromeOptions()
    for item in options:
        chrome_options.add_argument(item)
    # chrome_options.add_argument('--headless')
    # 不打印不重要的日志信息
    # chrome_options.add_argument('log-level=2')

    if sys.platform == 'linux':
        browser = webdriver.Chrome(executable_path='../driver/chromedriver_linux',
                                   chrome_options=chrome_options)
    else:
        browser = webdriver.Chrome(executable_path='../driver/chromedriver_mac',
                                   chrome_options=chrome_options)
    return browser
