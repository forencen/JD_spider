import os
import json
import time


def get_cookies(key=None):
    if os.path.exists('cookies.json'):
        with open('cookies.json', mode='r', encoding='utf-8') as f:
            res = json.load(f)
            ts = int(time.time())
            main_expiry = min([item.get('expiry', 999999999999999) for item in res])
            if main_expiry < ts:
                return None

            if key:
                v = [item.get('value') for item in res if item.get('name') == key]
                return v[0] if v else None
            else:
                return res
    else:
        return None


def write_cookies(cookies):
    with open('cookies.json', mode='w', encoding='utf-8') as f:
        json.dump(cookies, f)
