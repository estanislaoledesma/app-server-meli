# coding: utf-8
from flask_restful import Resource, reqparse
from flask import request
from ..settings import errorhandler, responsehandler
from flask_api import status
import pyrebase, pymongo, requests
from bson.objectid import ObjectId
from . import purchases
import datetime

TOKEN = 1

class Deliveries(Resource):

    DELIVERIES_URL = "http://localhost:8080/deliveries/estimate"
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

            purchase = self.mongo.db.purchases.find_one({'_id': ObjectId(purchase_id)})
            self.logger.info('purchase : %s', purchase)

            product = self.mongo.db.products.find_one({'_id': ObjectId(purchase ['product_id'])})
            self.logger.info('product : %s', product)

            purchase_state = purchase ['state']
            if (purchase_state > purchases.Purchases.PURCHASE_CHECKOUT):
                error = errorhandler.ErrorHandler(status.HTTP_409_CONFLICT, 'Ya se estableció una entrega.')
                return error.get_error_response()

            origin_address_str = product ['ubication']
            origin_latitude = product ['latitude']
            origin_longitude = product ['longitude']
            distance = self.gmaps.distance_matrix([origin_latitude, origin_longitude],
                                                  [destination_latitude, destination_longitude],
                                                  mode = 'driving') ["rows"] [0] ["elements"] [0] ["distance"] ["value"]
            distance = 10

            origin_location = {'lat': origin_latitude, 'lon': origin_longitude}
            destination_location = {'lat': destination_latitude, 'lon': destination_longitude}

            origin_address = {'street': origin_address_str, 'location': origin_location}
            destination_address = {'street': destination_address_str, 'location': destination_location}

            origin_endpoint = {'location': origin_address, 'timestamp': datetime.datetime.now()}
            destination_endpoint = {'location': destination_address, 'timestamp': datetime.datetime.now()}

            delivery = {}
            delivery ['applicationOwner'] = user ['userId']
            delivery ['start'] = origin_endpoint
            delivery ['end'] = destination_endpoint
            delivery ['distance'] = distance
            delivery ['value'] = purchase ['value']
            delivery ['route'] = ''
            delivery ['cost'] = {'currency': product ['currency'], 'value': 0}

            delivery_id = self.mongo.db.deliveries.insert_one(delivery).inserted_id

            delivery ['id'] = str(delivery_id)

            response = requests.post(url = self.DELIVERIES_URL, params = delivery)

            if response.status_code != status.HTTP_200_OK:
                error_message = response.reason
                error = errorhandler.ErrorHandler(status.HTTP_503_SERVICE_UNAVAILABLE, error_message)
                return error.get_error_response()

            cost = response.json() ['value']
            delivery ['cost'] ['value'] = cost

            self.mongo.db.deliveries.update_one({'_id': ObjectId(delivery_id)}, {'$set': delivery})

            tracking = {}
            tracking ['id'] = str(delivery_id)
            tracking ['status'] = ""
            tracking ['updateAt'] = 0

            response = requests.post(url = self.TRACKING_URL, params = tracking)

            if response.status_code != status.HTTP_201_CREATED:
                error_message = response.reason
                error = errorhandler.ErrorHandler(status.HTTP_503_SERVICE_UNAVAILABLE, error_message)
                return error.get_error_response()

            purchase_update = {'delivery_id': str(delivery_id), 'state': purchases.Purchases.PURCHASE_CHECKOUT_DELIVERY}
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

            parser = reqparse.RequestParser()
            parser.add_argument('destination_address')
            parser.add_argument('destination_latitude')
            parser.add_argument('destination_longitude')
            args = parser.parse_args()
            destination_address_str = args ['destination_address']
            destination_latitude = args ['destination_latitude']
            destination_longitude = args ['destination_longitude']

            purchase = self.mongo.db.purchases.find_one({'_id': ObjectId(purchase_id)})
            self.logger.info('purchase : %s', purchase)

            product = self.mongo.db.products.find_one({'_id': ObjectId(purchase ['product_id'])})
            self.logger.info('product : %s', product)

            purchase_state = purchase ['state']
            if (purchase_state > purchases.Purchases.PURCHASE_CHECKOUT):
                error = errorhandler.ErrorHandler(status.HTTP_409_CONFLICT, 'Ya se estableció una entrega.')
                return error.get_error_response()

            origin_address_str = product ['ubication']
            origin_latitude = product ['latitude']
            origin_longitude = product ['longitude']
            distance = self.gmaps.distance_matrix([origin_latitude, origin_longitude],
                                                  [destination_latitude, destination_longitude],
                                                  mode = 'driving') ["rows"] [0] ["elements"] [0] ["distance"] ["value"]
            distance = 0

            origin_location = {'lat': origin_latitude, 'lon': origin_longitude}
            destination_location = {'lat': destination_latitude, 'lon': destination_longitude}

            origin_address = {'street': origin_address_str, 'location': origin_location}
            destination_address = {'street': destination_address_str, 'location': destination_location}

            origin_endpoint = {'location': origin_address, 'timestamp': datetime.datetime.now()}
            destination_endpoint = {'location': destination_address, 'timestamp': datetime.datetime.now()}

            delivery = {}
            delivery['id'] = 0
            delivery ['applicationOwner'] = user ['userId']
            delivery ['start'] = origin_endpoint
            delivery ['end'] = destination_endpoint
            delivery ['distance'] = distance
            delivery ['value'] = distance
            delivery ['route'] = ''
            delivery ['cost'] = {'currency': product ['currency'], 'value': 0}

            response = requests.post(url = self.DELIVERIES_URL, params = delivery)

            if response.status_code != status.HTTP_200_OK:
                error_message = response.reason
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