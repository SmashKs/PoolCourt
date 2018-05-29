import requests


class InstagramRequest:
    def __init__(self, username, password):
        self.__username = username
        self.__password = password
        self.__requests = requests.session()
        self.__HEADERS = {
            'authority': 'www.instagram.com',
            'method': 'POST',
            'path': '/accounts/login/ajax',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,ja;q=0.5',
            'content-length': '70',
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': 'mid=WPDNwQAEAAFlEKzsk0lvqB-Mj4y4; ig_dru_dismiss=1501688703184; ig_lang=en; mcd=3; rur=FRC; csrftoken=lBOiWdTai69cdkTcM6B2BjJyGngzQjwp; urlgen="{"time": 1527388820}:1fMtSl:FXKN0-RFssC7PeJtcCkrYhCvZrg',
            'origin': 'https://www.instagram.com',
            'referer': 'https://www.instagram.com/',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            'x-csrftoken': 'lBOiWdTai69cdkTcM6B2BjJyGngzQjwp',
            'x-instagram-ajax': '8958fe1e75ab',
            'x-requested-with': 'XMLHttpRequest'
        }
        self.__login()

    def __login(self):
        data = {'username': self.__username, 'password': self.__password}
        response = self.__requests.post('https://www.instagram.com/accounts/login/ajax/', data=data, headers=self.__HEADERS)
        return response.status_code

    def get(self, url, headers='', cookies=''):
        return self.__requests.get(url, headers=headers, cookies=cookies)
