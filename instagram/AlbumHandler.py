from bs4 import BeautifulSoup
import re
from selenium import webdriver
from instagram.InstagramConstants import PHOTO_NEXT_BUTTON, PHOTO_PREV_BUTTON
import time


ALBUM_URL = 'https://www.instagram.com/p/BgURvYOlVSR/?taken-by=annehathaway'
USER = 'annehathaway'


class AlbumHandler(object):
    def __init__(self, album_url, user):
        self.__album_url = album_url
        self.__instagram_user = user
        self.__likes = -1
        self.__date = '1911/1/1'
        self.__photos = []
        self.__browser = webdriver.PhantomJS()
        self.__browser.get(self.__album_url)

    def get_likes(self):
        soup = BeautifulSoup(self.__browser.page_source, 'lxml')
        result = soup.find_all('span')
        for r in result:
            find = re.search('<span>([\d\,]+)</span>\slikes</span>', str(r))
            if find:
                self.__likes = int(find.group(1).replace(',', ''))
                return True
        return False

    def get_date(self):
        soup = BeautifulSoup(self.__browser.page_source, 'lxml')
        result = soup.find_all('time')
        for r in result:
            find = re.match("([\d\w:-]+)\.\d+\w", r['datetime'])
            if find:
                time.strftime(time.strptime(find.group(1), "%Y-%m-%dT%H:%M:%S"), "%Y/%m/%d")
                return True
        return False

    def get_photos(self):
        while True:
            soup = BeautifulSoup(self.__browser.page_source, 'lxml')
            imgs = soup.find_all('img')
            for img in imgs:
                if re.search("alt", str(img)):
                    self.__photos.append(img['src'])

            if not self.next_button():
                break
        return len(self.__photos)

    def get_reply_count(self):
        pass

    def next_button(self):
        if len(self.__browser.page_source) == 0:
            return False

        soup = BeautifulSoup(self.__browser.page_source, 'lxml')
        results = soup.find_all('div')
        for result in results:
            r = re.search("([_\d\w]+)\s+([_\d\w]+)\s+coreSpriteRightChevron", str(result))
            if r:
                next_button = 'a.' + r.group(1) + '.' + r.group(2) + '.' + PHOTO_NEXT_BUTTON
                self.__browser.find_element_by_css_selector(next_button).click()
                return True
        return False

    def previous_button(self):
        if len(self.__browser.page_source) == 0:
            return False

        soup = BeautifulSoup(self.__browser.page_source, 'lxml')
        results = soup.find_all('div')
        for result in results:
            r = re.search("([_\d\w]+)\s+([_\d\w]+)\s" + PHOTO_PREV_BUTTON, str(result))
            if r:
                next_button = 'a.' + r.group(1) + '.' + r.group(2) + '.' + PHOTO_PREV_BUTTON
                self.__browser.find_element_by_css_selector(next_button)
                return True
        return False


def main():
    album = AlbumHandler(ALBUM_URL, USER)
    album.get_photos()


if __name__ == '__main__':
    main()
