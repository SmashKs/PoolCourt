from datetime import datetime
from pprint import pprint as pp


class ImageDataObj:
    def __init__(self, source=None, detail=None):
        """
        @type detail: ImageDetailObj
        @type source: str
        """
        # The website or storage space where the photo stores.
        self.source = source  # type: str
        self.detail = detail  # type: ImageDetailObj

    def __iter__(self):
        if not self.source:
            raise ValueError('source must be input')

        yield self.source, dict(self.detail)


class ImageDetailObj:
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


if __name__ == '__main__':
    obj = ImageDataObj('ptt', ImageDetailObj())
    pp(dict(obj))
