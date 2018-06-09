from instagram.InstagramRequest import InstagramRequest
from instagram.MainPageParser import MainPageParser
from instagram.AlbumHandler import AlbumHandler


class Instagram:
    def __init__(self, username, password):
        self.__request = InstagramRequest()
        self.__album_handler = AlbumHandler()
        self.__request.login(username, password)

    def __del__(self):
        self.__request.logout()

    def search(self, keyword):
        pass

    def upload(self, photos):
        pass

    def get_photos(self, user_id):
        main_page = MainPageParser(user_id, self.__request)
        albums = main_page.run()
        for album in albums:
            self.__album_handler.run(album)
            photos = self.__album_handler.get_photos()
            for photo in photos:
                print(photos[photo])
