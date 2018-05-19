import time

from selenium import webdriver
from selenium.webdriver.android.webdriver import WebDriver


class LoginModule:
    def __init__(self, phantom_js):
        self.__browser = phantom_js  # type: WebDriver

    def login(self, user, pwd):
        self.__browser.get('https://www.instagram.com/accounts/login/')
        time.sleep(2)  # Wait for the user & password text view appear.
        self.__browser.find_element_by_xpath("//input[@name='username']").send_keys(user)
        self.__browser.find_element_by_xpath("//input[@name='password']").send_keys(pwd)
        self.__browser.find_element_by_xpath("//button[contains(.,'Log in')]").click()
        time.sleep(2)  # Wait the login process finish.


if __name__ == '__main__':
    login = LoginModule(webdriver.PhantomJS())
