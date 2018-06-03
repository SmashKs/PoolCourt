import re
import time
import requests
import json

from bs4 import BeautifulSoup


ALBUM_URL = 'https://www.instagram.com/p/BgURvYOlVSR/?taken-by=annehathaway'
USER = 'annehathaway'


class AlbumHandler:
    def __init__(self, album_url, user):
        self.__album_url = album_url
        self.user = user
        self.status_code = 0
        self.__metadata = {}

    def run(self):
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
        for node in self.__metadata['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']:
            photos_list[node['node']['id']] = node['node']['display_resources'][2]['src']

        return photos_list

    def get_tags(self):
        pass

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


def main():
    album = AlbumHandler('https://www.instagram.com/p/BjaMA2GFAty/?taken-by=annehathaway', 'annehathaway')
    album.run()
    print('status: ' + str(album.status_code))
    print(album.get_photos())
    print('comment count: ' + str(album.get_comment_count()))
    print('like count: ' + str(album.get_like_count()))
    print('timestamp: ' + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(album.get_post_time()))))


if __name__ == '__main__':
    main()
