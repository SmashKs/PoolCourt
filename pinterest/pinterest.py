import requests
import json
import re

from bs4 import BeautifulSoup
from http import HTTPStatus


class PhotoAnalyzer:
    def __init__(self):
        self.__url = ''
        self.__metadata = {}

    def run(self, url):
        self.__url = url
        if not self.__get_metadata():
            return False
        return True

    def __get_metadata(self):
        if len(self.__url) == 0:
            self.__metadata = ''
            return False

        response = requests.get(self.__url)
        if response.status_code != HTTPStatus.OK:
            print('status code: ' + str(response.status_code))
            return False

        soup = BeautifulSoup(response.content.decode(), 'lxml')
        result = soup.find('script', type='application/json', id='jsInit1')
        if result:
            self.__metadata = json.loads(result.string)
        else:
            self.__metadata = ''

        return True

    def get_photo_url(self):
        if len(self.__metadata) == 0:
            return ''

        return self.__metadata['resourceDataCache'][0]['data']['images']['orig']['url']

    def get_author(self):
        if len(self.__metadata) == 0:
            return ''

        return self.__metadata['resourceDataCache'][0]['data']['pinner']['full_name']

    def get_title(self):
        if len(self.__metadata) == 0:
            return ''

        return self.__metadata['resourceDataCache'][0]['data']['page_metadata']['og:description']

    def get_comment_count(self):
        if len(self.__metadata) == 0:
            return 0

        return self.__metadata['resourceDataCache'][0]['response']['data']['aggregated_pin_data']['comment_count']

    def get_like_count(self):
        if len(self.__metadata) == 0:
            return 0

        return self.__metadata['resourceDataCache'][0]['response']['data']['like_count']

    def get_post_time(self):
        if len(self.__metadata) == 0:
            return ''

        return self.__get_date(self.__metadata['resourceDataCache'][0]['data']['created_at'])

    def get_tags(self):
        if len(self.__metadata) == 0:
            return {}

        hash_tags = self.__metadata['resourceDataCache'][0]['data']['hashtags']
        tags = dict()
        for tag in hash_tags:
            t = tag.replace('#', '')
            tags[t] = 'https://www.pinterest.com/search/pins/?q=%23' + t + '&rs=hashtag_closeup'
        return tags

    @staticmethod
    def __get_date(timestamp):
        month_table = {
            'jan': '01',
            'feb': '02',
            'mar': '03',
            'apr': '04',
            'may': '05',
            'jun': '06',
            'jul': '07',
            'aug': '08',
            'sep': '09',
            'oct': '10',
            'nov': '11',
            'dec': '12',
        }

        r = re.search("[\w]+, ([\d]+) ([\w]+) ([\d]+) ([\d:]+)", timestamp)
        day = str(r.group(1))
        month = month_table[r.group(2).lower()]
        year = str(r.group(3))
        times = r.group(4)

        return year + '-' + month + '-' + day + ' ' + times


def main():
    url = 'https://www.pinterest.com/pin/500744052297425468/'
    a = PhotoAnalyzer()
    a.run(url)
    print('title: ' + a.get_title())
    print('author: ' + a.get_author())
    print('url: ' + a.get_photo_url())
    print('comment count: ' + str(a.get_comment_count()))
    print('like count: ' + str(a.get_like_count()))
    print(a.get_tags())
    print('post time: ' + a.get_post_time())


if __name__ == '__main__':
    main()
