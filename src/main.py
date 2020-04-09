from login import login
from order_info import get_order_info
from utils import get_cookies

if __name__ == '__main__':
    # 登陆
    cookies = get_cookies()
    if not cookies:
        cookies = login()
    get_order_info(cookies)

