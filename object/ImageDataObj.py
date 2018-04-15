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
    def __init__(self, uri=None, tags=None, likes=0, author=None, date=datetime.now()):
        self.uri = uri  # type: str
        # The comments were set while the author was uploading the photo.
        self.tags = tags  # type: dict
        # The number of likes which the photo was liked from friends and customers.
        self.likes = likes  # type: int
        # The user who uploaded the photo.
        self.author = author  # type: str
        self.date = date  # type: datetime

    def __iter__(self):
        yield 'uri', self.uri
        yield 'tag', self.tags
        yield 'count', self.likes
        yield 'date', self.date.strftime('%Y-%m-%d %H:%M')


if __name__ == '__main__':
    obj = ImageDataObj('ptt', ImageDetailObj())
    pp(dict(obj))
