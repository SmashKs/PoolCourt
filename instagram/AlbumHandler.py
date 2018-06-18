import re
import requests
import json

from bs4 import BeautifulSoup


class AlbumHandler:
    def __init__(self):
        self.__album_url = ''
        self.status_code = 0
        self.__metadata = {}

    def __init_metadata(self):
        self.__album_url = ''
        self.status_code = 0
        self.__metadata = {}

    def run(self, album_url):
        self.__init_metadata()
        self.__album_url = album_url

        response = requests.get(self.__album_url)
        self.status_code = response.status_code
        if response.status_code != 200:
            return

        soup = BeautifulSoup(response.content.decode(), 'lxml')
        results = soup.find_all('script', type='text/javascript')
        for result in results:
            r = re.search("window._sharedData =", str(result))
            if r:
                json_part = result.string
                json_part = json_part[json_part.find('=') + 2: -1]
                print(json_part)
                self.__metadata = json.loads(json_part)
                break

    def get_photos(self):
        if len(self.__metadata) == 0:
            return {}

        photos_list = {}

        if not ('edge_sidecar_to_children' in self.__metadata['entry_data']['PostPage'][0]['graphql']['shortcode_media']):
            photos_list[self.__metadata['entry_data']['PostPage'][0]['graphql']['shortcode_media']['id']] = \
                self.__metadata['entry_data']['PostPage'][0]['graphql']['shortcode_media']['display_resources'][2]['src']
            return photos_list

        for node in self.__metadata['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']:
            if not node['node']['is_video']:
                photos_list[node['node']['id']] = node['node']['display_resources'][2]['src']

        return photos_list

    def get_tags(self):
        response = requests.get(self.__album_url)
        if response.status_code != 200:
            return []

        tags = {}
        soup = BeautifulSoup(response.content.decode(), 'lxml')
        results = soup.find_all('meta', property='instapp:hashtags')
        for result in results:
            tags[result['content']] = 'https://www.instagram.com/explore/tags/' + result['content']

        return tags

    def get_comment_count(self):
        if len(self.__metadata) == 0:
            return -1

        return int(self.__metadata['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_to_comment']['count'])

    def get_like_count(self):
        if len(self.__metadata) == 0:
            return -1

        return int(self.__metadata['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_preview_like']['count'])

    def get_post_time(self):
        if len(self.__metadata) == 0:
            return -1

        return int(self.__metadata['entry_data']['PostPage'][0]['graphql']['shortcode_media']['taken_at_timestamp'])

    def get_short_code(self):
        if len(self.__metadata) == 0:
            return ''

        return self.__metadata['entry_data']['PostPage'][0]['graphql']['shortcode_media']['shortcode']

    def get_author(self):
        if len(self.__metadata) == 0:
            return ''

        return self.__metadata['entry_data']['PostPage'][0]['graphql']['shortcode_media']['owner']['username']
