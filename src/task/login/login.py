import base64
import getpass
import json
import os
import time

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import CONFIG
from tools.web_utils import init_browser
from tools.web_utils import write_cookies
from tools.logger_helper import logger
from tools.verificatio_helper import find_pic, get_tracks


def get_account_pwd():
    if os.path.exists("../resources/login.txt"):
        with open('../resources/login.txt', 'r', encoding='utf-8') as f:
            res = base64.b64decode(f.read())
            res = json.loads(res.decode())
            account, pwd = res.get('account'), res.get('pwd')
    else:
        account = input("用户名:")
        pwd = getpass.getpass("密码:")

    return account, pwd


def login_photo_validate(login_browser):
    try:
        template = login_browser.find_element_by_xpath(
            '//*[@id="JDJRV-wrap-loginsubmit"]/div/div/div/div[1]/div[2]/div[2]')
        template_base64 = login_browser.find_element_by_xpath(
            '//*[@id="JDJRV-wrap-loginsubmit"]/div/div/div/div[1]/div[2]/div[2]/img').get_attribute('src')
        bg_base64 = login_browser.find_element_by_xpath(
            '//*[@id="JDJRV-wrap-loginsubmit"]/div/div/div/div[1]/div[2]/div[1]/img').get_attribute('src')
        template_image_data = base64.b64decode(template_base64.split(',')[1])
        file_name = str(int(time.time()))
        template_name = 'template_%s.png' % file_name
        bg_name = 'bg_%s.png' % file_name
        with open('../captcha/%s' % template_name, 'wb') as f:
            f.write(template_image_data)
        bg_image_data = base64.b64decode(bg_base64.split(',')[1])
        with open('../captcha/%s' % bg_name, 'wb') as f:
            f.write(bg_image_data)
        x, _ = find_pic('../captcha/%s' % bg_name, '../captcha/%s' % template_name)
        # tracks = swipe(x)
        x = x - (38 / 2)
        # logger.info('bg: %s, template: %s, %s', (bg_name, template_name, x))
        offsets, tracks = get_tracks(x, 1, 'ease_out_expo')
        ActionChains(login_browser).click_and_hold(template).perform()
        for item in tracks:
            ActionChains(login_browser).move_by_offset(xoffset=item, yoffset=0).perform()
        time.sleep(1)
        ActionChains(login_browser).release().perform()

    except NoSuchElementException as e:
        return False


def login():
    login_browser = init_browser()
    wait_login = WebDriverWait(login_browser, CONFIG['WAIT_TIME'])
    login_browser.get('https://jd.com')
    # 登录界面
    login_browser.get(CONFIG['LOGIN_URL'])
    account_login_btn = login_browser.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div/div[3]/a')
    account_login_btn.click()
    time.sleep(1.5)

    # 获取本定的用户名/密码
    account, pwd = get_account_pwd()
    login_browser.find_element_by_xpath('//*[@id="loginname"]').send_keys(account)
    time.sleep(1.2)
    login_browser.find_element_by_xpath('//*[@id="nloginpwd"]').send_keys(pwd)
    time.sleep(1.3)
    login_browser.find_element_by_xpath('//*[@id="loginsubmit"]').click()
    time.sleep(1.4)
    # 循环检测是否登陆
    try_login_count = 0
    while True:
        if try_login_count > CONFIG.get('MAX_LOGIN_TIME', 10):
            logger.error('登录失败,超过最大登录次数:%s' % CONFIG.get('MAX_LOGIN_TIME', 10))
            return False
        try:
            wait_login.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                '#ttbar-login > div.dt.cw-icon > a'))
            )
            break
        except TimeoutException:
            logger.info('start login %s' % (try_login_count + 1))
            login_photo_validate(login_browser)
            try_login_count += 1

    logger.info('登陆成功！')
    time.sleep(2)
    with open('../resources/login.txt', 'w', encoding='utf-8') as f:
        f.write(base64.b64encode(json.dumps({'account': account, 'pwd': pwd}).encode()).decode())
    cookies = login_browser.get_cookies()
    write_cookies(cookies)
    # 关闭登陆浏览器
    login_browser.quit()
    return cookies
