import json
import re
import requests

from bs4 import BeautifulSoup

from instagram.InstagramLogin import LoginModule
from instagram.InstagramRequest import InstagramRequest

INSTAGRAM = 'https://www.instagram.com'


class MainPageParser:
    def __init__(self, username):
        self.__username = username
        self.__url = INSTAGRAM + '/' + self.__username
        self.__content = ''
        self.status_code = -1
        self.__metadata = {}
        self.__requests = requests.session()
        self.get_data()

    def get_data(self):
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
            if not node['node']['is_video']:
                album_list.append(node['node']['shortcode'])

        return album_list

    def query_page(self):
        user_id = self.get_user_id()
        end_cursor = self.get_end_cursor()
        query_hash = self.get_query_hash()
        albums = []
        query = self.QueryPage(self.__requests, user_id, query_hash, end_cursor)
        for i in range(0, int(self.get_album_count()/3)-1):
            if not query.query():
                break
            a = query.get_albums()
            for album in a:
                albums.append(album)
        return albums

    def run(self, username, password):
        self.login(username, password)
        output = []
        albums = self.get_albums()
        for album in albums:
            output.append('https://www.instagram.com/p/' + album + '/?taken-by=' + self.__username)

        query = self.QueryPage(self.__requests, self.get_user_id(), self.get_query_hash(), self.get_end_cursor())
        while query.query():
            albums = query.get_albums()
            for album in albums:
                output.append('https://www.instagram.com/p/' + album + '/?taken-by=' + self.__username)

        return output

    class QueryPage:
        def __init__(self, request, user_id, query_hash, end_cursor):
            self.__user_id = user_id
            self.__query_hash = query_hash
            self.__end_cursor = end_cursor
            self.__content = {}
            self.__requests = request

        def query(self):
            if not self.__end_cursor:
                return False
            instagram_query = 'https://www.instagram.com/graphql/query/?query_hash='
            cmd = instagram_query + self.__query_hash + '&variables=%7B%22id%22%3A%22' + self.__user_id + \
                  '%22%2C%22first%22%3A12%2C%22after%22%3A%22' + self.__end_cursor + '%22%7D'
            response = self.__requests.get(cmd)
            if response.status_code != 200:
                self.__content = {}
                return False

            self.__content = json.loads(response.content.decode())
            self.update_end_cursor()
            return True

        def update_end_cursor(self):
            if len(self.__content) == 0:
                return
            self.__end_cursor = self.__content['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']

        def get_albums(self):
            if len(self.__content) == 0:
                return []

            album_list = []
            for node in self.__content['data']['user']['edge_owner_to_timeline_media']['edges']:
                if not node['node']['is_video']:
                    album_list.append(node['node']['shortcode'])
            return album_list
