import datetime
import os
import re
import time
from http import HTTPStatus
from pprint import pprint as pp

import requests
from bs4 import BeautifulSoup

from __init__ import HOT_LEVEL, MAX_LIST_COUNT, PTT_BEAUTY_URL, PTT_URL


class PTTSpider(object):
    def __init__(self):
        self.__max_lists = MAX_LIST_COUNT  # type: int
        self.__hot_level = HOT_LEVEL  # type: int
        self.__list_content = None  # type: str

    def next_page(self, url):
        """
        @type url: str
        """
        text = self.__get_page_source(url)
        soup = BeautifulSoup(text, 'lxml')
        s = soup.find('div', 'btn-group btn-group-paging')
        tags = s.find_all('a', href=True)
        for tag in tags:
            if tag.text.strip() == '‹ 上頁':
                return PTT_URL + '/' + tag['href']

    def get_lists(self, board_url):
        """
        @type board_url: str
        """
        text = self.__get_page_source(board_url)
        soup = BeautifulSoup(text, 'lxml')
        titles = soup.find_all('div', 'r-ent')
        for t in titles:
            title = t.find('div', 'title').text.strip()
            hot_level = t.find('div', 'nrec').text.strip()
            if hot_level == '爆':
                hot_level = '100'
            url = t.find('a', href=True)
            author = t.find('div', 'author').text
            date = '2018/' + t.find('div', 'date').text.strip()
            mark = t.find('div', 'mark').text.strip()
            if author != '-':
                yield {
                    'title': title,
                    'hot_level': int(0 if len(hot_level) == 0 else hot_level),
                    'url': '' if url is None else PTT_URL + url['href'],
                    'date': time.mktime(datetime.datetime.strptime(date, '%Y/%m/%d').timetuple()),
                    'author': author,
                    'mark': False if len(mark) == 0 else True
                }

    def get_content(self, url):
        """
        @type url: str
        """
        text = self.__get_page_source(url)
        soup = BeautifulSoup(text, 'lxml')
        contents = soup.find_all('a', href=True)
        for content in contents:
            r = re.search('^(https).*(jpg)$', content['href'])
            if r:
                yield str(content['href'])

    def get_photo(self, url, fold_path=''):
        """
        @type fold_path: str
        @type url: str
        """
        if len(fold_path) == 0:
            fold_path = os.getcwd()
        r = requests.get(url)
        if r.status_code == HTTPStatus.OK:
            path = fold_path + '/' + (re.search('/(\w+\.jpg)$', url)).group(1)
            with open(path, 'wb') as f:
                f.write(r.content)

    def __get_page_source(self, url):
        """
        @type url: str
        """
        if not self.is_ptt_alive():
            return None
        response = requests.get(url)
        if response.status_code == HTTPStatus.OK:
            return response.text
        return None

    def is_ptt_alive(self):
        response = requests.get(PTT_URL)
        if response.status_code == HTTPStatus.OK:
            return True
        return False

    def set_max_lists(self, num=MAX_LIST_COUNT):
        """
        setting the condition about max lists
        @type num: int
        """
        self.__max_lists = num

    def set_hot_level(self, level=HOT_LEVEL):
        """
        setting the condition about hot level
        @type level: int
        """
        self.__hot_level = level

    def run(self):
        """
        starting spider
        @rtype: dict
        """
        if not self.is_ptt_alive():
            pp('PTT is not alive')
            return

        count = 0
        data = []
        now = PTT_BEAUTY_URL
        while True:
            for l in self.get_lists(now):
                if int(l['hot_level']) < int(self.__hot_level):
                    continue
                photos = []
                for photo in self.get_content(l['url']):
                    photos.append(photo)
                l.update({'photos': photos})
                data.append(l)
                count += 1
                if count == self.__max_lists:
                    return data
            now = self.next_page(now)


if __name__ == '__main__':
    spider = PTTSpider()
    pp(spider.run())
