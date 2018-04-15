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
    def __init__(self, uri='', tags=None, likes=0, author='', date=datetime.now()):
        """
        @type uri: str
        @type tags: list
        @type likes: int
        @type author: str
        @type date: datetime
        """
        # Setting a default value.
        if tags is None:
            tags = []

        # Checking the parameter is a None value.
        if uri is None or tags is None or likes is None or author is None or date is None:
            raise ValueError('The parameter must not be None.')

        self.uri = uri
        # The comments were set while the author was uploading the photo.
        self.tags = tags
        # The number of likes which the photo was liked from friends and customers.
        self.likes = likes
        # The user who uploaded the photo.
        self.author = author
        self.date = date

    def __iter__(self):
        yield 'uri', self.uri
        yield 'tag', self.tags
        yield 'count', self.likes
        yield 'date', self.date.strftime('%Y-%m-%d %H:%M')


if __name__ == '__main__':
    obj = ImageDataObj('ptt', ImageDetailObj())
    pp(dict(obj))
