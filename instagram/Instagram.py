import datetime

from instagram.InstagramRequest import InstagramRequest
from instagram.MainPageParser import MainPageParser
from instagram.AlbumHandler import AlbumHandler
from firebase.FirebaseWrapper import ImageDataObj, ImageDetailObj2, FirebaseWrapper, IMAGE_VERSION_2


class Instagram:
    def __init__(self, username, password):
        self.__request = InstagramRequest()
        self.__album_handler = AlbumHandler()
        self.__request.login(username, password)
        self.__firebase = FirebaseWrapper().create()

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
            title = self.__album_handler.get_short_code()
            photos = self.__album_handler.get_photos()
            tags = self.__album_handler.get_tags()
            likes = self.__album_handler.get_like_count()
            author = self.__album_handler.get_author()
            comments = self.__album_handler.get_comment_count()
            post_date = datetime.datetime.fromtimestamp(self.__album_handler.get_post_time())
            img = ImageDetailObj2(title=title,
                                  url_list=photos,
                                  tag_list=tags,
                                  author=author,
                                  likes=likes,
                                  comments=comments,
                                  date=post_date)
            self.__firebase.write_image_properties(author, dict(ImageDataObj(title, img)), IMAGE_VERSION_2)
