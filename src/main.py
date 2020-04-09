from login import login
from order_info import click_jd_hot_try
from utils import get_cookies

if __name__ == '__main__':
    # 登陆
    cookies = get_cookies()
    if not cookies:
        cookies = login()
    # 热点试用
    click_jd_hot_try(cookies)

