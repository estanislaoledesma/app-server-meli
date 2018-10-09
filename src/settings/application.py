# coding: utf-8
from flask import Flask
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_pymongo import PyMongo
from src.routes import hello, user, products
from .config import Config
import logging
import pyrebase

app = Flask(__name__)
api = Api(app)
ma = Marshmallow(app)

# Configuracion de Firebase
firebase = pyrebase.initialize_app(Config.setup)

#Configuracion de mongodb
#app.config["MONGO_URI"] = "mongodb://localhost:27017/meli_db"
mongo = PyMongo(app)
db = mongo.db

# Configuracion del logger
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

api.add_resource(hello.HelloWorld, '/', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(user.SignUp, '/signup', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(user.Login, '/login', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(products.Products, '/products', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})




