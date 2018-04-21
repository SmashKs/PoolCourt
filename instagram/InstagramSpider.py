from bs4 import BeautifulSoup
from selenium import webdriver
import re
from instagram.InstagramConstants import WEB_URL, USER_TAKEN, PHOTO_NEXT_BUTTON, PHOTO_PREV_BUTTON


INSTAGRAM_USER = "annehathaway"


class InstagramSpider(object):
    def __init__(self, user):
        self.__current_page_content = ''
        self.__web_browser = webdriver.PhantomJS()
        self.__instagram_user = user

        # properties
        self.__date = '19110101'

    def get_list(self):
        browser = webdriver.PhantomJS()
        browser.get(WEB_URL + '/' + INSTAGRAM_USER)

        albums = re.findall("<a href=\"(/p[\/\d\w]+)\/", browser.page_source)
        if len(albums) == 0:
            return None

        for album in albums:
            yield WEB_URL + album + USER_TAKEN + INSTAGRAM_USER

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
                next_button = 'a.' + r.group(1) + '.' + r.group(2) + '.' + PHOTO_NEXT_BUTTON
                self.__web_browser.find_element_by_css_selector(next_button).click()
                return True
        return False

    def previous_button(self):
        if len(self.__current_page_content) == 0:
            return False

        soup = BeautifulSoup(self.__current_page_content, 'lxml')
        results = soup.find_all('div')
        for result in results:
            r = re.search("([_\d\w]+)\s+([_\d\w]+)\s" + PHOTO_PREV_BUTTON, str(result))
            if r:
                next_button = 'a.' + r.group(1) + '.' + r.group(2) + '.' + PHOTO_PREV_BUTTON
                self.__web_browser.find_element_by_css_selector(next_button)
                return True
        return False

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, date):
        self.__date = date

    def run(self):
        pass
