# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup


class PTTSpider(object):
    def __init__(self):
        self.PTT_URL = "https://www.ptt.cc"
        self.PTT_INDEX_URL = "https://www.ptt.cc/bbs/index.html"
        self.__boards = None

    def get_boards(self):
        text = self.__get_page_source(self.PTT_INDEX_URL)
        if text is None:
            return None

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

    def get_lists(self, board_url):
        text = self.__get_page_source(board_url)
        soup = BeautifulSoup(text, 'lxml')
        titles = soup.find_all('div', 'r-ent')
        for t in titles:
            title = t.find('div', "title")
            hot_level = t.find('div', 'nrec')
            url = t.find('a', href=True)
            yield {
                "title": title.text.strip(),
                "hot_level": str(0 if len(hot_level.text) == 0 else hot_level.text),
                "url": "" if url is None else url['href']
            }

    def get_content(self, index):
        pass

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


def main():
    ptt = PTTSpider()
    if not ptt.is_ptt_alive():
        print("ptt is off line")
        return

    for board in ptt.get_boards():
        print(board)


if __name__ == '__main__':
    main()
