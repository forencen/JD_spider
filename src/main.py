from hot_try import click_jd_hot_try
from login import login
from utils import get_cookies


def run():
    # 登陆
    cookies = get_cookies()
    if not cookies:
        cookies = login()
    if not cookies:
        return
    # 热点试用
    click_jd_hot_try(cookies)


if __name__ == '__main__':
    run()

