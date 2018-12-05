# coding: utf-8
import os

from flask import Flask
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_pymongo import PyMongo
from src.routes import hello, user, products, product, \
    purchases, payments, deliveries, questions, answers, \
    search, ping, rating, activity, statistics
import logging
import pyrebase
import requests
from datetime import datetime
import time

app = Flask(__name__)
api = Api(app)
ma = Marshmallow(app)

# Configuracion de Firebase
setup = {
        "apiKey": "AIzaSyD3s0dTCy3J4v_3FitnlF_K2qTzsevIIBg",
        "authDomain": "meli-4620b.firebaseapp.com",
        "databaseURL": "https://meli-4620b.firebaseio.com",
        "storageBucket": "meli-4620b.appspot.com",
        "serviceAccount": 'src/settings/meli-4620b-firebase-adminsdk-8c1z7-b12f7ba600.json'
    }
firebase = pyrebase.initialize_app(setup)

#Configuracion de mongodb
MONGO_URL = os.environ.get('MONGO_URL')
if not MONGO_URL:
    MONGO_URL = "mongodb://localhost:27017/meli_db";

app.config['MONGO_URI'] = MONGO_URL
mongo = PyMongo(app)
db = mongo.db

SHARED_SERVER_URL = "http://localhost:8080/server"

server = {}
server ['_rev'] = str(time.mktime(datetime.now().timetuple()))
server ['createdBy'] = 'Developer'
server ['createdTime'] = time.mktime(datetime.now().timetuple())
server ['name'] = 'Meli'
server ['lastConnection'] = time.mktime(datetime.now().timetuple())

server_id = str(mongo.db.servers.insert_one(server).inserted_id)
server ['id'] = server_id
server.pop('_id', None)

# Configuracion del logger
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

response = requests.post(url = SHARED_SERVER_URL, json = server)
app.logger.info(response.content)

api.add_resource(hello.HelloWorld, '/', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(user.SignUp, '/users/signup', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(user.Login, '/users/login', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(user.User, '/users/<user_id>', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(products.Products, '/products', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(product.Product, '/products/<product_id>', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(purchases.Purchases, '/products/<product_id>/purchases', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(payments.Payments, '/purchases/<purchase_id>/payments', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(deliveries.Deliveries, '/purchases/<purchase_id>/deliveries', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(questions.Questions, '/products/<product_id>/questions', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(answers.Answers, '/questions/<question_id>/answers', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(search.Search, '/products/search', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(ping.Ping, '/ping', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(rating.Rating, '/users/<user_id>/score', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(deliveries.Estimates, '/products/<product_id>/deliveries/estimate', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(activity.MyPurchases, '/mypurchases', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(activity.MySales, '/mysales', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(deliveries.DeliveryStatus, '/deliveries/<tracking_id>', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(payments.PaymentStatus, '/payments/<payment_id>', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo})
api.add_resource(statistics.StatsUsers, '/stats/users', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo, 'server_id': server_id})
api.add_resource(statistics.StatsSales, '/stats/sales', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo, 'server_id': server_id})
api.add_resource(statistics.StatsProducts, '/stats/products', resource_class_kwargs={'logger': app.logger, 'firebase': firebase, 'mongo': mongo, 'server_id': server_id})








