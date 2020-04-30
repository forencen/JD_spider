import json
import logging.handlers
import os
import sys

from selenium import webdriver

log_file = '../log/logger.log'
LOGGING_MSG_FORMAT = '[%(asctime)s] [%(levelname)s] [%(module)s] [%(funcName)s] [%(lineno)d] %(message)s'
time_handler = logging.handlers.TimedRotatingFileHandler(log_file, when='D', interval=1, backupCount=0)
time_handler.suffix = '%Y-%m-%d.log'
time_handler.setLevel('INFO')  # error以上的内容输出到文件里面
formatter = logging.Formatter(LOGGING_MSG_FORMAT)
time_handler.setFormatter(formatter)
logger = logging.getLogger('JD')
logger.setLevel('INFO')
logger.addHandler(time_handler)


def get_cookies(key=None):
    if os.path.exists('../resources/cookies.json'):
        with open('../resources/cookies.json', mode='r', encoding='utf-8') as f:
            res = json.load(f)
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
