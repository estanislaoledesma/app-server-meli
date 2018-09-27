from flask import Flask
from flask_restful import Api
from flask_marshmallow import Marshmallow
from src.routes import hello, user
from .config import Config
import logging
import pyrebase

app = Flask(__name__)
api = Api(app)
ma = Marshmallow(app)

# Configuracion de Firebase
firebase = pyrebase.initialize_app(Config.setup)


# Configuracion del logger
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

api.add_resource(hello.HelloWorld, '/', resource_class_kwargs={'logger': app.logger, 'firebase': firebase})
api.add_resource(user.Sign_Up, '/signup', resource_class_kwargs={'logger': app.logger, 'firebase': firebase})
api.add_resource(user.Login, '/login', resource_class_kwargs={'logger': app.logger, 'firebase': firebase})
