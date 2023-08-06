import hashlib
import json

import pyperclip
from requestspr import Requests

requests = Requests()


def request_get(url, params=None, **kwargs):
    return requests.get(url, params, **kwargs)


def request_post(url, data=None, json=None, **kwargs):
    return requests.post(url, data, json, **kwargs)


def md5(text):
    m = hashlib.md5()
    m.update(text.encode('utf-8'))
    return m.hexdigest()


def parse_headers(headers_str: str) -> dict:
    """
    将调试工具复制的header字符串转为dict类型
    """
    return dict(line.split(': ', maxsplit=1) for line in headers_str.split('\n'))


def parse_cookies(cookie_str: str) -> dict:
    """
    将header中的cookie字符串转成dict
    """
    return dict(item.split('=') for item in cookie_str.split('; '))


def format_data(data, _2dict: bool = True, copy: bool = True) -> str:
    """
    dict 或 list 或json字符串转化成格式化字符串
    :param data: 数据
    :param _2dict: 是否将转化成的json字符串再转化成python的dict字符串
    :param copy: 是否复制结果字符串（需要pyperclip依赖）
    :return 转化成的字符串
    """

    _type = type(data)
    print(_type)
    if _type == str:
        data = json.loads(data)
    elif _type != dict and _type != list:
        return ''
    result = json.dumps(data, indent=4, ensure_ascii=False)
    if _2dict:
        result = result.replace('null', 'None').replace('true', 'True').replace('false', 'False')
    if copy:
        pyperclip.copy(result)
    return result


def print_formatted_dict(data, _2dict: bool = True, copy: bool = True) -> str:
    """
    dict 或 list 或json字符串转化成格式化字符串并打印
    :param data: 数据
    :param _2dict: 是否将转化成的json字符串再转化成python的dict字符串
    :param copy: 是否复制结果字符串（需要pyperclip依赖）
    :return 转化成的字符串
    """
    result = format_data(data, _2dict, copy)
    print(result)
    return result
