import json
import re
from urllib import parse

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.ie.webdriver import WebDriver

from instagram.InstagramLogin import LoginModule

HEADERS = {
    "Origin": "https://www.instagram.com/",
    "Referer": "https://www.instagram.com/annehathaway/",
    "Authority": "www.instagram.com",
    "Scheme": "https",
    "Path": "/annehathaway/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/58.0.3029.110 Safari/537.36",
    "Host": "www.instagram.com",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,ja;q=0.5",
    "X-Instragram-AJAX": "1",
    "X-Requested-With": "XMLHttpRequest",
    "Upgrade-Insecure-Requests": "1",
}

INSTAGRAM = 'https://www.instagram.com'


class MainPageParser(object):
    def __init__(self, url):
        self.__browser = webdriver.PhantomJS()  # type: WebDriver
        self.__login_module = LoginModule(self.__browser)
        self.__url = url

    def run(self, username, password):
        # Before anything login to the Instragram.
        self.__login_module.login(username, password)

        self.__browser.get(self.__url)
        soup = BeautifulSoup(self.__browser.page_source, 'lxml')
        albums = re.findall("<a href=\"(/p[\/\d\w]+)\/", self.__browser.page_source)
        if len(albums) == 0:
            return None

        count = 0
        # for album in albums:
        #     count += 1
        #     print(album)
        # print('count: ' + str(count))

        # parser = MainPageParser2('annehathaway')
        # print(parser.query_cmd())

        # The fist step.
        query_hash = self.get_user_id(self.__browser.page_source)
        # The second step.
        user_id = self.get_id(self.__browser.page_source)
        # The third step.
        end_cursor = self.get_end_cursor(self.__browser.page_source)

        instagram_query = 'https://www.instagram.com/graphql/query/?query_hash='
        variables = dict()
        variables['id'] = user_id
        variables['first'] = 12
        variables['after'] = end_cursor
        cmd = instagram_query + query_hash + '&variables=' + str(variables).replace(' ', '').replace("'", '"')
        self.__browser.get(cmd)

        print(self.__browser.page_source)
        self.__get_response_json_content(self.__browser.page_source)

        # albums = re.findall("<a href=\"(/p[\/\d\w]+)\/", self.__browser.page_source)
        # if len(albums) == 0:
        #     return None
        #
        # count = 0
        # for album in albums:
        #     count += 1
        #     print(album)
        # print('count: ' + str(count))

    def get_id(self, content):
        soup = BeautifulSoup(content, 'lxml')
        results = soup.find_all('script', type='text/javascript', src=False)
        for result in results:
            if re.search("window._sharedData", str(result)):
                print(result)
                r = re.search(r'"owner":{"id":"(\d+)"}', str(result))
                if r:
                    return r.group(1)
        return None

    def get_user_id(self, content):
        soup = BeautifulSoup(content, 'lxml')
        result = soup.find('link', rel='preload', href=True)
        url = INSTAGRAM + result['href']
        # response = requests.get(url, headers=HEADERS)
        print('(get_user_id) url: ' + url)
        self.__browser.get(url)
        # print('(get_user_id) content: ' + self.__browser.page_source)
        # r = re.search("\},m=\"([\w\d]+)\",g=Object", self.__browser.page_source)
        #
        # return r.group(1)

        hash_id_list = re.findall(r'queryId:"(\w+)"', self.__browser.page_source)
        if not hash_id_list:
            print("Didn't find anything...")
            return []
        print(hash_id_list)

        self.__browser.back()

        return hash_id_list[1]

    def get_end_cursor(self, content):
        soup = BeautifulSoup(content, 'lxml')
        results = soup.find_all('script', type='text/javascript', src=False)
        for result in results:
            if re.search("window\._sharedData", str(result)):
                r = re.search("end_cursor\":\"([-_\d\w\.]+)\"", str(result))
                if r:
                    return r.group(1)
        return None

    def __get_response_json_content(self, content):
        soup = BeautifulSoup(content, 'lxml')
        json_content = soup.find('pre').text
        j = json.loads(json_content)
        edges = j['data']['user']['edge_owner_to_timeline_media']['edges']
        print(edges)
        for edge in edges:
            uri = edge['node']['display_url']
            print(uri)


class MainPageParser2(object):
    def __init__(self, user):
        self.__user = user
        self.__qq = requests.session()

    def get_end_cursor(self, content):
        soup = BeautifulSoup(content, 'lxml')
        results = soup.find_all('script', type='text/javascript', src=False)
        for result in results:
            if re.search("window\._sharedData", str(result)):
                r = re.search("end_cursor\":\"([-_\d\w\.]+)\"", str(result))
                if r:
                    return r.group(1)
        return None

    def get_query_hash(self, content):
        soup = BeautifulSoup(content, 'lxml')
        result = soup.find('link', rel='preload', href=True)
        url = INSTAGRAM + result['href']
        response = requests.get(url, headers=HEADERS)
        r = re.findall("queryId:\"([\w\d]+)\"", response.content.decode())
        return r[1]

    def get_id(self, content):
        soup = BeautifulSoup(content, 'lxml')
        results = soup.find_all('script', type='text/javascript', src=False)
        for result in results:
            if re.search("window\._sharedData", str(result)):
                r = re.search("\"id\":\"(\d+)\"", str(result))
                if r:
                    return r.group(1)
        return None

    def get_user_id(self, content):
        soup = BeautifulSoup(content, 'lxml')
        result = soup.find('link', rel='preload', href=True)
        url = INSTAGRAM + result['href']
        response = requests.get(url, headers=HEADERS)
        r = re.search("\},m=\"([\w\d]+)\",g=Object", response.content.decode())
        return r.group(1)

    def first_query(self):
        response = self.__qq.get(INSTAGRAM + '/' + self.__user, headers=HEADERS)
        query_hash = self.get_user_id(response.content.decode())
        query_id = self.get_id(response.content.decode())
        query_url = 'https://www.instagram.com/graphql/query/?query_hash='
        variables = dict()
        variables['user_id'] = query_id
        variables['include_chaining'] = 'false'
        variables['include_reel'] = 'false'
        variables['include_suggested_users'] = 'false'
        variables['include_logged_out_extras'] = 'true'
        variables['include_highlight_reels'] = 'false'
        url = query_url + query_hash + parse.quote(json.dumps(variables))
        print(dict(response.cookies))
        HEADERS['cookie'] = json.dumps(dict(response.cookies))
        print(HEADERS)  # get 403
        # response = requests.get(url, headers=HEADERS)
        # print('status: ' + str(response.status_code))
        # print('header: ' + str(response.headers))

    def test_by_selenium(self):
        browser = webdriver.PhantomJS()
        browser.get(INSTAGRAM + '/' + self.__user)
        print(browser.page_source)
        query_hash = self.get_user_id(browser.page_source)
        query_id = self.get_id(browser.page_source)
        end_cursor = self.get_end_cursor(browser.page_source)
        instagram_query = 'https://www.instagram.com/graphql/query/?query_hash='
        variables = dict()
        variables['id'] = query_id
        variables['first'] = 12
        variables['after'] = end_cursor
        cmd = instagram_query + query_hash + '&variables=%7B%22id%22%3A%22' + query_id + '%22%2C%22first%22%3A12%2C%22after%22%3A%22' + end_cursor + '%22%7D'
        print('url: ' + cmd)
        browser.get(cmd)
        print(browser.page_source)
        browser.close()

    def query_cmd(self):
        response = self.__qq.get(INSTAGRAM + '/' + self.__user, headers=HEADERS)
        query_hash = self.get_query_hash(response.content.decode())
        query_id = self.get_id(response.content.decode())
        end_cursor = self.get_end_cursor(response.content.decode())
        instagram_query = 'https://www.instagram.com/graphql/query/?query_hash='
        variables = dict()
        variables['id'] = query_id
        variables['first'] = 12
        variables['after'] = end_cursor
        # cmd = instagram_query + query_hash + '&variables=' + parse.quote(json.dumps(variables))
        cmd = instagram_query + query_hash + '&variables=%7B%22id%22%3A%22' + query_id + '%22%2C%22first%22%3A12%2C%22after%22%3A%22' + end_cursor + '%22%7D'
        response = self.__qq.get(cmd, cookies=response.cookies)
        print('status: ' + str(response.status_code))
        print(response.headers)
        return cmd

    def test(self):
        response = self.__qq.get(INSTAGRAM + '/' + self.__user, headers=HEADERS)
        print('status: ' + str(response.status_code))
        print('headers: ' + str(response.headers))
        print('cookies')
        print(str(response.cookies))
        self.get_profile_page_container(response.content.decode())


def main():
    # response = requests.get('https://www.instagram.com/annehathaway', headers=HEADERS)
    main_page = MainPageParser('https://www.instagram.com/annehathaway')
    main_page.run()


if __name__ == '__main__':
    main()
