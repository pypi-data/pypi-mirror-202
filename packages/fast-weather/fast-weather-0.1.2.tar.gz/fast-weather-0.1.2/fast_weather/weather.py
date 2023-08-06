import requests


def get_now():
    r = requests.get('http://www.weather.com.cn/data/sk/101020100.html')
    r.encoding = 'utf-8'
    return r.json()


def who_are_you():
    return "一个帅哥"
