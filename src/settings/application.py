from flask import Flask
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow
from src.routes import hello, user
import firebase_admin
from firebase_admin import credentials
from . import config
import logging
from logging.handlers import RotatingFileHandler
import pyrebase

app = Flask(__name__)
api = Api(app)
ma = Marshmallow(app)

# Configuracion de Firebase
conf = config.Config()
cred = credentials.Certificate(conf.get_fb_credentials())
fb_app = firebase_admin.initialize_app(cred)
firebase = pyrebase.initialize_app(conf.get_websetup())


# Configuracion del logger
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

api.add_resource(hello.HelloWorld, '/', resource_class_kwargs={'logger': app.logger}, endpoint='hello')
api.add_resource(user.Sign_Up, '/signup', resource_class_kwargs={'logger': app.logger})
api.add_resource(user.Login, '/login', resource_class_kwargs={'logger': app.logger})
