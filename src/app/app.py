import firebase_admin
from flask import Flask
from firebase_admin import credentials
from . import config

class App(object):

    def __init__(self):
        conf = config.Config()
        cred = credentials.Certificate(conf.get_fb_credentials())
        self.fb_app = firebase_admin.initialize_app(cred)
        self.app = Flask(__name__)

    def get_app(self):
        return self.app

    def get_fb_app(self):
        return self.default_app

    def run(self):
        self.app.run()