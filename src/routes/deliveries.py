# coding: utf-8
from flask_restful import Resource, reqparse
from flask import request
from ..settings import errorhandler, responsehandler
from flask_api import status
import pyrebase, pymongo, requests
from bson.objectid import ObjectId
from . import purchases
import datetime
import geopy.distance

TOKEN = 1

def getDistance(origin, destination):
    distance = geopy.distance.distance(origin, destination).km
    return distance

class Deliveries(Resource):

    PENDING_DELIVERY = 5
    DELIVERY_IN_PROGRESS = 6
    DELIVERED = 7

    DELIVERY_STATUS = {PENDING_DELIVERY: 'Entrega Pendiente',
                       DELIVERY_IN_PROGRESS: 'Entrega en proceso',
                       DELIVERED: 'Entrega Realizada'}

    DELIVERIES_URL = "http://localhost:8080/delivery/estimate"
    TRACKING_URL = "http://localhost:8080/tracking"

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
        self.mongo = kwargs.get('mongo')
        self.firebase = kwargs.get('firebase')
        self.gmaps = kwargs.get('gmaps')

    def post(self, purchase_id):
        try:
            # Authentication
            auth_header = request.headers.get('Authorization')
            auth_token = auth_header.split(" ")[TOKEN]
            auth = self.firebase.auth()
            user = auth.refresh(auth_token)

            json_data = request.get_json(force=True)
            destination_address_str = json_data ['destination_address']
            destination_latitude = json_data ['destination_latitude']
            destination_longitude = json_data['destination_longitude']
            destination = [destination_latitude, destination_longitude]

            purchase = self.mongo.db.purchases.find_one({'_id': ObjectId(purchase_id)})
            self.logger.info('purchase : %s', purchase)

            product = self.mongo.db.products.find_one({'_id': ObjectId(purchase ['product_id'])})
            self.logger.info('product : %s', product)

            origin_address_str = product ['ubication']
            origin_latitude = product ['latitude']
            origin_longitude = product ['longitude']
            origin = [origin_latitude, origin_longitude]

            distance = getDistance(origin, destination)
            self.logger.info('distance : %s', distance)

            origin_location = {'lat': origin_latitude, 'lon': origin_longitude}
            destination_location = {'lat': destination_latitude, 'lon': destination_longitude}

            origin_address = {'street': origin_address_str, 'location': origin_location}
            destination_address = {'street': destination_address_str, 'location': destination_location}

            origin_endpoint = {'location': origin_address, 'timestamp': datetime.datetime.now()}
            destination_endpoint = {'location': destination_address, 'timestamp': datetime.datetime.now()}

            user_data = self.mongo.db.users.find_one({'uid': user ['userId']})
            self.logger.info('user : %s', product)

            purchase_amount = self.mongo.db.purchases.find({'user_id': user ['userId']}).count()
            self.logger.info('purchase amount : %s', purchase_amount)

            delivery = {}
            delivery ["distance"] = distance
            delivery ["value"] = purchase ['value']
            delivery ["userscore"] = 0
            delivery ["mail"] = user_data ['email']
            delivery ["purchaseQuantity"] = purchase_amount
            self.logger.info('request : %s', str(delivery))

            response = requests.post(url = self.DELIVERIES_URL, json = delivery)

            if response.status_code != status.HTTP_200_OK:
                self.logger.info('response : %s', response.content)
                error_message = response.content
                error = errorhandler.ErrorHandler(status.HTTP_503_SERVICE_UNAVAILABLE, error_message)
                return error.get_error_response()

            cost = response.json() ['cost']
            delivery ['cost'] = cost

            delivery_id = self.mongo.db.deliveries.insert_one(delivery).inserted_id

            tracking = {}
            tracking ['id'] = str(delivery_id)
            tracking ['status'] = Deliveries.DELIVERY_STATUS [Deliveries.PENDING_DELIVERY]

            response = requests.post(url = self.TRACKING_URL, json = tracking)

            if response.status_code != status.HTTP_201_CREATED:
                error_message = response.content
                error = errorhandler.ErrorHandler(status.HTTP_503_SERVICE_UNAVAILABLE, error_message)
                return error.get_error_response()

            purchase_update = {'delivery_id': str(delivery_id)}
            self.mongo.db.purchases.update_one({'_id': ObjectId(purchase_id)}, {'$set': purchase_update})

            response_data  = response.json()
            response = responsehandler.ResponseHandler(status.HTTP_200_OK, response_data)
            response.add_autentication_header(user['refreshToken'])
            return response.get_response()

        except IndexError as e:
            error = errorhandler.ErrorHandler(status.HTTP_401_UNAUTHORIZED, 'Debe autenticarse previamente.')
            return error.get_error_response()

        except pyrebase.pyrebase.HTTPError as e:
            error_message = errorhandler.get_error_message(e)
            error = errorhandler.ErrorHandler(status.HTTP_400_BAD_REQUEST, error_message)
            return error.get_error_response()

        except pymongo.errors.PyMongoError as e:
            error = errorhandler.ErrorHandler(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Surgió un problema inesperado')
            return error.get_error_response()


    def get(self, purchase_id):
        try:
            # Authentication
            auth_header = request.headers.get('Authorization')
            auth_token = auth_header.split(" ")[TOKEN]
            auth = self.firebase.auth()
            user = auth.refresh(auth_token)

            purchase = self.mongo.db.purchases.find_one({'_id': ObjectId(purchase_id)})
            self.logger.info('purchase : %s', purchase)

            delivery = self.mongo.db.deliveries.find_one({'_id': ObjectId(purchase ['delivery_id'])})
            self.logger.info('delivery : %s', delivery)

            delivery ['_id'] = str(delivery ['_id'])

            response_data  = delivery
            response = responsehandler.ResponseHandler(status.HTTP_200_OK, response_data)
            response.add_autentication_header(user['refreshToken'])
            return response.get_response()

        except IndexError as e:
            error = errorhandler.ErrorHandler(status.HTTP_401_UNAUTHORIZED, 'Debe autenticarse previamente.')
            return error.get_error_response()

        except pyrebase.pyrebase.HTTPError as e:
            error_message = errorhandler.get_error_message(e)
            error = errorhandler.ErrorHandler(status.HTTP_400_BAD_REQUEST, error_message)
            return error.get_error_response()

        except pymongo.errors.PyMongoError as e:
            error = errorhandler.ErrorHandler(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Surgió un problema inesperado')
            return error.get_error_response()


class Estimates(Resource):

    DELIVERIES_URL = "http://localhost:8080/delivery/estimate"
    TRACKING_URL = "http://localhost:8080/tracking"

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
        self.mongo = kwargs.get('mongo')
        self.firebase = kwargs.get('firebase')
        self.gmaps = kwargs.get('gmaps')

    def get(self, product_id):
        try:
            # Authentication
            auth_header = request.headers.get('Authorization')
            auth_token = auth_header.split(" ")[TOKEN]
            auth = self.firebase.auth()
            user = auth.refresh(auth_token)

            parser = reqparse.RequestParser()
            parser.add_argument('destination_address')
            parser.add_argument('destination_latitude')
            parser.add_argument('destination_longitude')
            args = parser.parse_args()
            destination_address_str = args ['destination_address']
            destination_latitude = args ['destination_latitude']
            destination_longitude = args ['destination_longitude']
            destination = [destination_latitude, destination_longitude]

            product = self.mongo.db.products.find_one({'_id': ObjectId(product_id)})
            self.logger.info('product : %s', product)

            origin_address_str = product ['ubication']
            origin_latitude = product ['latitude']
            origin_longitude = product ['longitude']
            origin = [origin_latitude, origin_longitude]

            distance = getDistance(origin, destination)
            self.logger.info('distance : %s', distance)

            origin_location = {'lat': origin_latitude, 'lon': origin_longitude}
            destination_location = {'lat': destination_latitude, 'lon': destination_longitude}

            origin_address = {'street': origin_address_str, 'location': origin_location}
            destination_address = {'street': destination_address_str, 'location': destination_location}

            origin_endpoint = {'location': origin_address, 'timestamp': datetime.datetime.now()}
            destination_endpoint = {'location': destination_address, 'timestamp': datetime.datetime.now()}

            user_data = self.mongo.db.users.find_one({'uid': user ['userId']})
            self.logger.info('user : %s', product)

            purchase_amount = self.mongo.db.purchases.find({'user_id': user ['userId']}).count()
            self.logger.info('purchase amount : %s', purchase_amount)

            delivery = {}
            delivery['id'] = 0
            delivery ['distance'] = distance
            delivery ['value'] = product ['price']
            delivery ['userscore'] = 0
            delivery ['mail'] = user_data ['email']
            delivery ['purchaseQuantity'] = purchase_amount


            response = requests.post(url = self.DELIVERIES_URL, json = delivery)

            if response.status_code != status.HTTP_200_OK:
                error_message = response.content
                error = errorhandler.ErrorHandler(status.HTTP_503_SERVICE_UNAVAILABLE, error_message)
                return error.get_error_response()

            cost = response.json()

            response_data  = cost
            response = responsehandler.ResponseHandler(status.HTTP_200_OK, response_data)
            response.add_autentication_header(user['refreshToken'])
            return response.get_response()

        except IndexError as e:
            error = errorhandler.ErrorHandler(status.HTTP_401_UNAUTHORIZED, 'Debe autenticarse previamente.')
            return error.get_error_response()

        except pyrebase.pyrebase.HTTPError as e:
            error_message = errorhandler.get_error_message(e)
            error = errorhandler.ErrorHandler(status.HTTP_400_BAD_REQUEST, error_message)
            return error.get_error_response()

        except pymongo.errors.PyMongoError as e:
            error = errorhandler.ErrorHandler(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Surgió un problema inesperado')
            return error.get_error_response()

class DeliveryStatus(Resource):

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
        self.mongo = kwargs.get('mongo')
        self.firebase = kwargs.get('firebase')
        self.gmaps = kwargs.get('gmaps')

    def put(self, delivery_id):
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                raise IndexError

            auth_token = auth_header.split(" ")[TOKEN]
            auth = self.firebase.auth()
            user = auth.refresh(auth_token)

        except IndexError as e:
            error = errorhandler.ErrorHandler(status.HTTP_401_UNAUTHORIZED, 'Debe autenticarse previamente.')
            return error.get_error_response()

        except AttributeError as e:
            error = errorhandler.ErrorHandler(status.HTTP_401_UNAUTHORIZED, 'Debe autenticarse previamente.')
            return error.get_error_response()

        try:
            json_data = request.get_json(force=True)
            self.logger.info('edit delivery: %s', json_data)
            new_status = json_data ['status']

            self.mongo.db.deliveries.update_one({"_id": ObjectId(delivery_id)}, {'$set': {'status': new_status}})

            response_data = {}
            response = responsehandler.ResponseHandler(status.HTTP_200_OK, response_data)
            response.add_autentication_header(user['refreshToken'])
            return response.get_response()

        except ValueError as e:
            error = errorhandler.ErrorHandler(status.HTTP_400_BAD_REQUEST, 'Bad info')
            return error.get_error_response()

        except pyrebase.pyrebase.HTTPError as e:
            error_message = errorhandler.get_error_message(e)
            error = errorhandler.ErrorHandler(status.HTTP_400_BAD_REQUEST, error_message)
            return error.get_error_response()