# -*- coding:utf-8 -*-

import requests
import re
import os
import datetime
import time
from bs4 import BeautifulSoup


PTT_BEAUTY_URL = "https://www.ptt.cc/bbs/Beauty/index.html"


class PTTSpider(object):
    def __init__(self):
        self.PTT_URL = "https://www.ptt.cc"
        self.PTT_INDEX_URL = "https://www.ptt.cc/bbs/index.html"
        self.__max_lists = 20
        self.__hot_level = 0
        self.__list_content = None

    def next_page(self, url):
        text = self.__get_page_source(url)
        soup = BeautifulSoup(text, 'lxml')
        s = soup.find("div", "btn-group btn-group-paging")
        tags = s.find_all('a', href=True)
        for tag in tags:
            if tag.text.strip() == '‹ 上頁':
                return self.PTT_URL + "/" + tag['href']

    def get_lists(self, board_url):
        text = self.__get_page_source(board_url)
        soup = BeautifulSoup(text, 'lxml')
        titles = soup.find_all('div', 'r-ent')
        for t in titles:
            title = t.find('div', "title").text.strip()
            hot_level = t.find('div', 'nrec').text.strip()
            if hot_level == '爆':
                hot_level = '100'
            url = t.find('a', href=True)
            author = t.find('div', 'author').text
            date = "2018/" + t.find('div', 'date').text.strip()
            mark = t.find('div', 'mark').text.strip()
            if author != '-':
                yield {
                    'title': title,
                    'hot_level': int(0 if len(hot_level) == 0 else hot_level),
                    'url': "" if url is None else self.PTT_URL + url['href'],
                    'date': time.mktime(datetime.datetime.strptime(date, "%Y/%m/%d").timetuple()),
                    'author': author,
                    'mark': False if len(mark) == 0 else True
                }

    def get_content(self, url):
        text = self.__get_page_source(url)
        soup = BeautifulSoup(text, 'lxml')
        contents = soup.find_all('a', href=True)
        for content in contents:
            r = re.search("^(https).*(jpg)$", content['href'])
            if r:
                yield str(content['href'])

    def get_photo(self, url, fold_path=""):
        if len(fold_path) == 0:
            fold_path = os.getcwd()
        r = requests.get(url)
        if r.status_code == 200:
            path = fold_path + "/" + (re.search("/(\w+\.jpg)$", url)).group(1)
            with open(path, 'wb') as f:
                f.write(r.content)

    def __get_page_source(self, url):
        if not self.is_ptt_alive():
            return None
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None

    def is_ptt_alive(self):
        response = requests.get(self.PTT_URL)
        if response.status_code == 200:
            return True
        return False

    '''
    setting the condition about max lists
    '''
    def set_max_lists(self, num=20):
        self.__max_lists = num

    '''
    setting the condition about hot level
    '''
    def set_hot_level(self, level=0):
        self.__hot_level = level

    '''
    starting spider
    '''
    def run(self):
        if not self.is_ptt_alive():
            print("PTT is not alive")
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
