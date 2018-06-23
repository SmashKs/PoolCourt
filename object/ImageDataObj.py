from datetime import datetime
from pprint import pprint as pp


class ImageDataObj:
    def __init__(self, album_id=None, detail=None):
        """
        @type detail: ImageDetailBase
        @type album_id: str
        """
        # The website or storage space where the photo stores.
        self.album_id = album_id  # type: str
        self.detail = detail  # type: ImageDetailBase

    def __iter__(self):
        if not self.album_id:
            raise ValueError('source must be input')

        yield self.album_id, dict(self.detail)


class ImageDetailBase:
    def __iter__(self):
        pass


class ImageDetailObj(ImageDetailBase):
    # The parameters doesn't allow to assign `None` value.
    def __init__(self, title='', uri_list=None, tag_list=None, likes=0, author='', date=datetime.now()):
        """
        @type title: str
        @type uri_list: list
        @type tag_list: list
        @type likes: int
        @type author: str
        @type date: datetime
        """
        # Setting a default value.
        if uri_list is None:
            uri_list = []
        if tag_list is None:
            tag_list = []

        # Checking the parameter is a None value.
        self.__parameters_checker(author, date, likes, tag_list, uri_list)

        self.__title = title
        self.__uri_list = uri_list
        # The comments were set while the author was uploading the photo.
        self.__tag_list = tag_list
        # The number of likes which the photo was liked from friends and customers.
        self.__likes = likes
        # The user who uploaded the photo.
        self.__author = author
        self.__date = date

    def __iter__(self):
        yield 'title', self.__title
        yield 'uri', self.__uri_list
        yield 'tag', self.__tag_list
        yield 'count', self.__likes
        yield 'date', self.__date.strftime('%Y-%m-%d %H:%M')

    @staticmethod
    def __parameters_checker(author, date, likes, tag_list, uri_list):
        if uri_list is None or tag_list is None or likes is None or author is None or date is None:
            raise ValueError('The parameter must not be None.')


class ImageDetailObj2(ImageDetailBase):
    def __init__(self,
                 title='',
                 author='',
                 url_list=None,
                 tag_list=None,
                 likes=0,
                 comments=0,
                 date=datetime.now()):
        """
        @type title: str
        @type author: str
        @type url_list: dict
        @type tag_list: dict
        @type likes: int
        @type comments: int
        @type date: datetime

        :param title: the title of this album
        :param author: the owner of this album
        :param url_list: {id: photo url}
        :param tag_list: {tag string: tag url}
        :param likes: the number of likes
        :param comments: the number of comments
        :param date: timestamp
        """

        self.__title = title
        self.__author = author
        self.__url_list = url_list
        self.__tag_list = tag_list
        self.__likes = likes
        self.__comments = comments
        self.__date = date

    def __iter__(self):
        yield 'author', self.__author
        yield 'title', self.__title
        yield 'uri', self.__url_list
        yield 'tag', self.__tag_list
        yield 'likes', self.__likes
        yield 'comments', self.__comments
        yield 'post date', self.__date.strftime('%Y-%m-%d %H:%M')

    def __parameters_checker(self):
        if self.__title is None:
            raise ValueError('The parameter title is invalid.')
        if self.__author is None:
            raise ValueError('The parameter author is invalid.')
        if self.__url_list is None or not isinstance(self.__url_list, dict):
            raise ValueError('The parameter url_list is invalid.')
        if self.__tag_list is None or not isinstance(self.__tag_list, dict):
            raise ValueError('The parameter tag_list is invalid.')
        if self.__likes is None:
            raise ValueError('The parameter likes is invalid.')
        if self.__comments is None:
            raise ValueError('The parameter comments is invalid.')
        if self.__date is None:
            raise ValueError('The parameter date is invalid.')


if __name__ == '__main__':
    obj = ImageDataObj('ptt', ImageDetailObj())
    pp(dict(obj))
