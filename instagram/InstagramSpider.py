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
        self.__likes = 0

    def get_list(self):
        browser = webdriver.PhantomJS()
        browser.get(WEB_URL + '/' + INSTAGRAM_USER)

        albums = re.findall("<a href=\"(/p[\/\d\w]+)\/", browser.page_source)
        if len(albums) == 0:
            return None

        for album in albums:
            yield WEB_URL + album + USER_TAKEN + INSTAGRAM_USER

    def get_album_metadata(self, album_url):
        browser = webdriver.PhantomJS()
        browser.get(album_url)
        self.__current_page_content = browser.page_source

    def get_photos(self, url):
        pass


    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, date):
        self.__date = date

    def run(self):
        pass
