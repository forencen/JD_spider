from hot_try import click_jd_hot_try
from login import login
from utils import get_cookies, init_browser, is_login


def run():
    # 登陆
    cookies = get_cookies()
    login_browser = init_browser(options=['--headless', 'log-level=2'])
    if not is_login(login_browser, cookies):
        cookies = login(login_browser)
    if not cookies:
        return
    # 热点试用
    click_jd_hot_try(cookies)


if __name__ == '__main__':
    run()
