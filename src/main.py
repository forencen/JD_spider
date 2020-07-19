from task.hot_try.hot_try import click_jd_hot_try
from task.login.login import login
from tools.web_utils import get_cookies
from tools.web_utils import is_login


def run():
    cookies = get_cookies()
    if not cookies or not is_login(cookies):
        cookies = login()
    if not cookies:
        return
    # 热点试用
    click_jd_hot_try(cookies)


if __name__ == '__main__':
    run()
