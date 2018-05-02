import requests
from bs4 import BeautifulSoup
import re
import json
from urllib import parse

HEADERS = {
    "Origin": "https://www.instagram.com/",
    "Referer": "https://www.instagram.com/morisakitomomi/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/58.0.3029.110 Safari/537.36",
    "Host": "www.instagram.com",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, sdch, br",
    "accept-language": "en-US;q=0.8,en;q=0.7",
    "X-Instragram-AJAX": "1",
    "X-Requested-With": "XMLHttpRequest",
    "Upgrade-Insecure-Requests": "1",
}

INSTAGRAM = 'https://www.instagram.com'


class MainPageParser(object):
    def __init__(self, user):
        self.__user = user

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

    def query_cmd(self, user):
        response = requests.get(user, headers=HEADERS)
        query_hash = self.get_query_hash(response.content.decode())
        query_id = self.get_id(response.content.decode())
        end_cursor = self.get_end_cursor(response.content.decode())
        instagram_query = 'https://www.instagram.com/graphql/query/?query_hash='
        variables = dict()
        variables['id'] = query_id
        variables['first'] = 12
        variables['after'] = end_cursor
        cmd = instagram_query + query_id + '&variables=' + parse.quote(json.dumps(variables))
        return cmd
