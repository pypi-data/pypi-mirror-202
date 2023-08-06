import requests
# import fast_weather


def get_now():
    r = requests.get('http://www.weather.com.cn/data/sk/101020100.html')
    r.encoding = 'utf-8'
    return r.json()


# print(get_now())