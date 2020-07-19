from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import CONFIG
from tools.web_utils import init_browser


class BaseTask:

    def __init__(self, uri=None):
        self.browser = init_browser()
        self.web_page = None
        if uri:
            self.web_page = self.browser.get(uri)
        self.wait_browser = WebDriverWait(self.browser, CONFIG['WAIT_TIME'])

    def set_cookies_to_browser(self, cookies):
        if cookies and isinstance(cookies, list):
            for cookie in cookies:
                if 'expiry' in cookie:
                    cookie['expiry'] = int(cookie['expiry'])
                self.browser.add_cookie(cookie)

    def get_web_page(self, uri):
        """
        或得浏览器页面信息
        :param uri: 跳转的uri
        :return:
        """
        if not uri:
            return self.web_page
        return self.browser.get(uri)

    def find_element(self, name, method='xpath'):
        """
        通过选择器得要页面元素
        :param name: 等待的目标元素选择器
        :param method: 等待的目标元素选择器类型
        :return:
        """
        if method == 'xpath':
            element = self.browser.find_element_by_xpath(name)
        elif method == 'css':
            element = self.browser.find_element_by_css_selector(name)
        else:
            element = None
        return element

    def wait_element(self, name, call_back, method='css', timeout=None):
        """
        等待一个元素的出现
        :param name: 等待的目标元素选择器
        :param call_back: 元素出现的回调函数
        :param method: 等待的目标元素选择器类型
        :param timeout: 等待超时时间
        :return: 1. 存在回调函数返回调用之后的值
                 2. 等待元素出现返回true
                 3. 超时后抛出TimeoutException
        """
        if timeout:
            self.wait_browser = WebDriverWait(self.browser, timeout)
        selector = By.CSS_SELECTOR if method == 'css' else By.XPATH

        self.wait_browser.until(
            EC.presence_of_element_located(
                (selector, name)
            )
        )

        if call_back and callable(call_back):
            return call_back()
        else:
            return True

    def run(self):
        """
        调度器将从run函数作为task入口
        :return:
        """
        raise NotImplemented

