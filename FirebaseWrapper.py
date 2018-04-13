class FirebaseWrapper(object):
    def __init__(self):
        self.__USER_CONFIG = 'smashksdevelop-config.json'
        self.__user_config = None
        self.__firebase = None

    def read_user_config(self):
        try:
            with open(self.__USER_CONFIG) as filp:
                self.__user_config = json.loads(filp.read())
        except FileNotFoundError as err:
            print(err)
            self.__user_config = None

    def connect(self):
        if self.__user_config:
            self.__firebase = pyrebase.initialize_app(self.__user_config)

    def upload(self):
        if self.__firebase:
            self.__firebase = None

    def write_image_properties(self, image):
        pass

    def read_image_properties(self):
        pass
