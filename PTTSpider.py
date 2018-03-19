# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup


class PTTSpider(object):
    def __init__(self):
        self.PTT_URL = "https://www.ptt.cc"
        self.PTT_INDEX_URL = "https://www.ptt.cc/bbs/index.html"

    def get_boards(self):
        text = self.__get_page_source(self.PTT_INDEX_URL)
        soup = BeautifulSoup(text, 'lxml')
        boards = soup.find_all('div', 'b-ent')
        for board in boards:
            board_url = board.find('a', href=True)
            board_name = board.find('div', 'board-name')
            board_title = board.find('div', 'board-title')
            board_class = board.find('div', 'board-class')
            board_user = board.find('div', 'board-nuser')
            yield {
                'name': board_name.text,
                'title': board_title.text,
                'class': board_class.text,
                'users': board_user.text,
                'url': self.PTT_URL + board_url['href']
            }

    def get_lists(self, board):
        pass

    def get_content(self, index):
        pass

    def __get_page_source(self, url):
        if not self.__is_ptt_alive():
            return None
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None

    def __is_ptt_alive(self):
        response = requests.get(self.PTT_URL)
        if response.status_code == 200:
            return True
        return False
