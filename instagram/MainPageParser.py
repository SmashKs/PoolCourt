import json
import re
from urllib import parse

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.ie.webdriver import WebDriver

from instagram.InstagramLogin import LoginModule
from instagram.InstagramRequest import InstagramRequest

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
        self.__user_id = ''
        self.__query_hash = ''

    def run(self, username, password):
        # Before anything login to the Instragram.
        self.__login_module.login(username, password)
        # Go to the a user page we wanna get.
        self.__browser.get(self.__url)

        # The fist step.
        self.__query_hash = self.get_user_id(self.__browser.page_source)
        # The second step.
        self.__user_id = self.get_id(self.__browser.page_source)
        # The third step.
        end_cursor = self.get_end_cursor(self.__browser.page_source)

        # Get the first page api.
        self.__jump_to_album_page(end_cursor)

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
        # print('(get_user_id) url: ' + url)
        self.__browser.get(url)
        # print('(get_user_id) content: ' + self.__browser.page_source)
        # r = re.search("\},m=\"([\w\d]+)\",g=Object", self.__browser.page_source)
        #
        # return r.group(1)

        hash_id_list = re.findall(r'queryId:"(\w+)"', self.__browser.page_source)
        if not hash_id_list:
            print("Didn't find anything...")
            return []

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

    def __jump_to_album_page(self, end_cursor):
        instagram_query = 'https://www.instagram.com/graphql/query/?query_hash='
        variables = dict()
        variables['id'] = self.__user_id
        variables['first'] = 12
        variables['after'] = end_cursor
        cmd = instagram_query + self.__query_hash + '&variables=' + str(variables).replace(' ', '').replace("'", '"')
        self.__browser.get(cmd)

    def __get_response_json_content(self, content):
        soup = BeautifulSoup(content, 'lxml')
        json_content = soup.find('pre').text
        j = json.loads(json_content)
        edges = j['data']['user']['edge_owner_to_timeline_media']['edges']

        for edge in edges:
            uri = edge['node']['display_url']
            print(uri)

        # Recursive pase the album.
        page_info = j['data']['user']['edge_owner_to_timeline_media']['page_info']
        if page_info['has_next_page']:
            self.__jump_to_album_page(page_info['end_cursor'])
            self.__get_response_json_content(self.__browser.page_source)


class MainPageParser2:
    def __init__(self, username, url):
        self.__username = username
        self.__url = url
        self.__content = ''
        self.status_code = -1
        self.__metadata = {}
        self.__requests = requests.session()

    def run(self):
        response = self.__requests.get(self.__url)
        self.__content = response.content.decode()
        self.status_code = response.status_code
        if self.status_code != 200:
            print('status code: ' + str(self.status_code))
            return

        # search window._sharedData
        soup = BeautifulSoup(self.__content, 'lxml')
        results = soup.find_all('script', type='text/javascript')
        for result in results:
            r = re.findall('window._sharedData =', str(result))
            if r:
                json_part = result.string
                print(json_part)
                self.__metadata = json.loads(json_part[json_part.find('=')+2: -1])
                break

    def login(self, username, password):
        HEADER = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4',
            'content-length': '23',
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': 'mid=V39AvQAEAAEIwy8g1C7EViIlodxd; s_network=; ig_pr=1; ig_vw=650; '
                      'csrftoken=3r8AwU3xWRhQMFIMz5b6ICn6Pfa4A5ZV',
            'origin': 'https://www.instagram.com',
            'referer': 'https://www.instagram.com/accounts/login/',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/51.0.2704.103 Safari/537.36',
            'x-csrftoken': '3r8AwU3xWRhQMFIMz5b6ICn6Pfa4A5ZV',
            'x-instagram-ajax': '1',
            'x-requested-with': 'XMLHttpRequest'
        }
        response = self.__requests.get('https://www.instagram.com/accounts/login')
        print('login status: ' + str(response.status_code))
        data = {'username': username, 'password': password}
        response = self.__requests.post('https://www.instagram.com/accounts/login/ajax/', data=data, headers=HEADER)
        print('login pose status: ' + str(response.status_code))

    def get_follower_count(self):
        if len(self.__metadata) == 0:
            return -1

        return int(self.__metadata['entry_data']['ProfilePage'][0]['graphql']['user']['edge_followed_by']['count'])

    def get_album_count(self):
        if len(self.__metadata) == 0:
            return -1

        return int(self.__metadata['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['count'])

    def is_verified_user(self):
        if len(self.__metadata) == 0:
            return False

        return self.__metadata['entry_data']['ProfilePage'][0]['graphql']['user']['is_verified']

    def get_user_id(self):
        if len(self.__metadata) == 0:
            return ''

        return self.__metadata['entry_data']['ProfilePage'][0]['graphql']['user']['id']

    def get_end_cursor(self):
        if len(self.__metadata) == 0:
            return ''

        return self.__metadata['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']

    def get_query_hash(self):
        soup = BeautifulSoup(self.__content, 'lxml')
        result = soup.find('link', rel='preload', href=True)
        url = INSTAGRAM + result['href']
        response = self.__requests.get(url, headers=HEADERS)
        r = re.findall("queryId:\"([\w\d]+)\"", response.content.decode())
        return r[1]

    def get_albums(self):
        if len(self.__metadata) == 0:
            return None

        album_list = []
        for node in self.__metadata['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']:
            album_list.append(node['node']['shortcode'])

        return album_list

    def query_page(self):
        user_id = self.get_user_id()
        end_cursor = self.get_end_cursor()
        query_hash = self.get_query_hash()
        print(self.__metadata)
        print('query_hash: ' + query_hash)
        instagram_query = 'https://www.instagram.com/graphql/query/?query_hash='
        cmd = instagram_query + query_hash + '&variables=%7B%22id%22%3A%22' + user_id + '%22%2C%22first%22%3A12%2C%22after%22%3A%22' + end_cursor + '%22%7D'
        response = self.__requests.get(cmd)
        print('status code: ' + str(response.status_code))
        return self.get_album_from_query(response.content.decode())

    def get_album_from_query(self, content):
        album_list = []
        metadata = json.loads(content)
        for node in metadata['data']['user']['edge_owner_to_timeline_media']['edges']:
            album_list.append(node['node']['shortcode'])
        return album_list


def main():
    pass


if __name__ == '__main__':
    main()
