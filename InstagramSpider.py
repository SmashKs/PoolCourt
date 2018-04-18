from bs4 import BeautifulSoup
from selenium import webdriver
import re


INSTAGRAM_USER = "annehathaway"
INSTAGRAM = "https://www.instagram.com"

GROUP_TAG = '_6d3hm _mnav9'
PHOTO_TAG = '_mck9w _gvoze  _tn0ps'

ALBUM = '/p/BhNP6DNFwi-'


class InstagramSpider(object):
    def __init__(self):
        self.__current_page_content = ''
        self.__web_browser = webdriver.PhantomJS()

    def get_list(self):
        browser = webdriver.PhantomJS()
        browser.get(INSTAGRAM + '/' + INSTAGRAM_USER)

        soup = BeautifulSoup(browser.page_source, 'lxml')
        groups = soup.find_all('div', GROUP_TAG)
        for group in groups:
            albums = group.find_all('a', href=True)
            for album in albums:
                print("url: " + INSTAGRAM + album['href'] + '?taken-by=' + INSTAGRAM_USER)

    def get_photos(self, url):
        pass

    def next_button(self):
        if len(self.__current_page_content) == 0:
            return False

        soup = BeautifulSoup(self.__current_page_content, 'lxml')
        results = soup.find_all('div')
        for result in results:
            r = re.search("([_\d\w]+)\s+([_\d\w]+)\s+coreSpriteRightChevron", str(result))
            if r:
                next_button = 'a.' + r.group(1) + '.' + r.group(2) + '.coreSpriteRightChevron'
                self.__web_browser.find_element_by_css_selector(next_button).click()
                return True
        return False

    def previous_button(self):
        if len(self.__current_page_content) == 0:
            return False

        soup = BeautifulSoup(self.__current_page_content, 'lxml')
        results = soup.find_all('div')
        for result in results:
            r = re.search("([_\d\w]+)\s+([_\d\w]+)\s+coreSpriteLeftChevron", str(result))
            if r:
                next_button = 'a.' + r.group(1) + '.' + r.group(2) + '.coreSpriteLeftChevron'
                self.__web_browser.find_element_by_css_selector(next_button).click()
                return True
        return False


def main():
    instagram = InstagramSpider()
    instagram.get_photos(ALBUM)


if __name__ == '__main__':
    main()
