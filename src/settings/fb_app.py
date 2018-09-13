import firebase_admin
from firebase_admin import credentials
from . import config

class FB_App(object):

    def __init__(self):
        conf = config.Config()
        cred = credentials.Certificate(conf.get_fb_credentials())
        self.fb_app = firebase_admin.initialize_app(cred)

    def get_fb_app(self):
        return self.fb_app