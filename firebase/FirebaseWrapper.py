import json
from pprint import pprint as pp

import pyrebase
from pyrebase.pyrebase import Auth, Database, Firebase, Storage

from firebase.__init__ import FIREBASE_CONFIGURATION
from object.ImageDataObj import ImageDataObj, ImageDetailObj

IMAGE_VERSION_1 = 'properties'


class FirebaseWrapper(object):
    def __init__(self):
        self.__USER_CONFIG = FIREBASE_CONFIGURATION
        self.__user_config = None  # type: dict
        self.__firebase = None  # type: Firebase
        # *** We don't use this `auth` now.
        self.__firebase_auth = None  # type: Auth
        self.__firebase_database = None  # type: Database
        self.__firebase_storage = None  # type: Storage

    def _load_user_config(self):
        try:
            with open(self.__USER_CONFIG) as file:
                self.__user_config = json.loads(file.read())
        except FileNotFoundError as err:
            pp(err)
            self.__user_config = None

    def _obtain_each_objects(self):
        if self.__user_config:
            self.__firebase = pyrebase.initialize_app(self.__user_config)
            # Get the firebase then assign each subjects.
            if self.__firebase:
                self.__firebase_auth = self.__firebase.auth()
                self.__firebase_database = self.__firebase.database()
                self.__firebase_storage = self.__firebase.storage()

    def create(self):
        """
        @rtype: FirebaseWrapper
        """
        self._load_user_config()
        self._obtain_each_objects()

        return self

    def upload(self):
        if self.__firebase:
            self.__firebase = None

    def write_image_properties(self, image_data=None):
        """
        @type image_data: dict
        """
        if not isinstance(image_data, dict):
            raise TypeError('image_data should be a dict object.')

        self.__firebase_database.child(IMAGE_VERSION_1).set(image_data)

    def read_image_properties(self):
        pass


if __name__ == '__main__':
    f = FirebaseWrapper().create()
    f.write_image_properties(dict(ImageDataObj('ptt', ImageDetailObj())))
