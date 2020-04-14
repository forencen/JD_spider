import base64
import getpass
import json
import os
import time

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config.config import CONFIG
from utils import get_cookies
from utils import write_cookies
from utils import init_browser


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
        btn_left = login_browser.find_element_by_xpath(
            '//*[@id="JDJRV-wrap-loginsubmit"]/div/div/div/div[2]/div[1]/div[1]')
        template_base64 = login_browser.find_element_by_xpath(
            '//*[@id="JDJRV-wrap-loginsubmit"]/div/div/div/div[1]/div[2]/div[2]/img').get_attribute('src')
        bg_base64 = login_browser.find_element_by_xpath(
            '//*[@id="JDJRV-wrap-loginsubmit"]/div/div/div/div[1]/div[2]/div[1]/img').get_attribute('src')
        template_image_data = base64.b64decode(template_base64.split(',')[1])
        with open('../resources/template.png', 'wb') as f:
            f.write(template_image_data)
        bg_image_data = base64.b64decode(bg_base64.split(',')[1])
        with open('../resources/bg.png', 'wb') as f:
            f.write(bg_image_data)

    except NoSuchElementException as e:
        return False



def login():
    login_browser = init_browser()
    wait_login = WebDriverWait(login_browser, CONFIG['WAIT_TIME'])
    login_browser.get('https://jd.com')
    cookies = get_cookies()
    if cookies:
        pass
    # 登录界面
    login_browser.get(CONFIG['LOGIN_URL'])
    account_login_btn = login_browser.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/div/div[3]/a')
    account_login_btn.click()
    time.sleep(1.5)

    # 获取本定的用户名/密码
    account, pwd = get_account_pwd()
    login_browser.find_element_by_xpath('//*[@id="loginname"]').send_keys(account)
    time.sleep(1)
    login_browser.find_element_by_xpath('//*[@id="nloginpwd"]').send_keys(pwd)
    time.sleep(1)
    login_browser.find_element_by_xpath('//*[@id="loginsubmit"]').click()
    time.sleep(1)
    # 循环检测是否登陆
    while True:
        try:
            wait_login.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                '#ttbar-login > div.dt.cw-icon > a'))
            )
            break
        except TimeoutException:
            login_photo_validate(login_browser)

    print('登陆成功！')
    time.sleep(2)
    with open('../resources/login.txt', 'w', encoding='utf-8') as f:
        f.write(base64.b64encode(json.dumps({'account': account, 'pwd': pwd}).encode()).decode())
    cookies = login_browser.get_cookies()
    write_cookies(cookies)
    # 关闭登陆浏览器
    login_browser.quit()
    return cookies


