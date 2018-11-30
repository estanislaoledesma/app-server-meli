# coding: utf-8
import os

from flask import Flask
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_pymongo import PyMongo
from src.routes import hello, user, products, product, \
    purchases, payments, deliveries, trackings, questions, answers, \
    search, ping, rating
from .config import Config
import logging
import pyrebase
import googlemaps
from datetime import datetime

app = Flask(__name__)
api = Api(app)
ma = Marshmallow(app)

# Configuracion de Firebase
firebase = pyrebase.initialize_app(Config.setup)

#Configuracion de mongodb
MONGO_URL = os.environ.get('MONGO_URL')
if not MONGO_URL:
    MONGO_URL = "mongodb://localhost:27017/meli_db";

app.config['MONGO_URI'] = MONGO_URL
mongo = PyMongo(app)
db = mongo.db

gmaps = googlemaps.Client(key = 'AIzaSyDd_fCIYbz8xiusm7RjuTHZBzuSlL-UAtw')

# Configuracion del logger
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

api.add_resource(hello.HelloWorld, '/', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(user.SignUp, '/users/signup', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(user.Login, '/users/login', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(user.User, '/users/<user_id>', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(products.Products, '/products', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(product.Product, '/products/<product_id>', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(purchases.Purchases, '/products/<product_id>/purchases', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(payments.Payments, '/purchases/<purchase_id>/payments', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(deliveries.Deliveries, '/purchases/<purchase_id>/deliveries', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo, 'gmaps': gmaps})
api.add_resource(trackings.Trackings, '/purchases/<purchase_id>/trackings', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo, 'gmaps': gmaps})
api.add_resource(questions.Questions, '/products/<product_id>/questions', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(answers.Answers, '/questions/<question_id>/answers', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(search.Search, '/products/search', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo, 'gmaps': gmaps})
api.add_resource(ping.Ping, '/ping', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(rating.Rating, '/score', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(deliveries.Estimates, '/products/<product_id>/deliveries/estimate', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo, 'gmaps': gmaps})
