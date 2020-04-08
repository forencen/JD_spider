import sys

from selenium import webdriver

from login import login

# 打开无界面的chrome浏览器
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
# 不打印不重要的日志信息
chrome_options.add_argument('log-level=2')

if sys.platform == 'linux':
    login_browser = webdriver.Chrome(executable_path='../driver/chromedriver_linux')
    browser = webdriver.Chrome(executable_path='../driver/chromedriver_linux',
                               chrome_options=chrome_options)
else:
    login_browser = webdriver.Chrome(executable_path='../driver/chromedriver_mac')
    browser = webdriver.Chrome(executable_path='../driver/chromedriver_linux',
                               chrome_options=chrome_options)


if __name__ == '__main__':
    # 登陆
    cookies = login(login_browser)
    for item in cookies:
        browser.add_cookie(item)

