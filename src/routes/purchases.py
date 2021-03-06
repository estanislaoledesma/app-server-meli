# coding: utf-8
from flask_restful import Resource
from flask import request
from ..settings import errorhandler, responsehandler
from flask_api import status
import pyrebase, pymongo
import datetime
from bson.objectid import ObjectId

TOKEN = 1


class InvalidStateException(Exception):
    pass


class Purchases(Resource):

    PURCHASE_CHECKOUT = 0
    PURCHASE_CHECKOUT_DELIVERY = 1
    PURCHASE_PENDING_PAYMENT_PROCESS = 2
    PURCHASE_PAYMENT_ACCEPTED = 3
    PURCHASE_PAYMENT_REJECTED = 4
    PURCHASE_PENDING_DELIVERY = 5
    PURCHASE_DELIVERY_IN_PROGRESS = 6
    PURCHASE_DELIVERED = 7

    PURCHASE_STATES = {PURCHASE_CHECKOUT: 'Checkout',
                       PURCHASE_CHECKOUT_DELIVERY: 'Delivery Checkout',
                       PURCHASE_PENDING_PAYMENT_PROCESS: 'Pago pendiente de proceso',
                       PURCHASE_PAYMENT_ACCEPTED: 'Pago Aceptado',
                       PURCHASE_PAYMENT_REJECTED: 'Pago Rechazado',
                       PURCHASE_PENDING_DELIVERY: 'Entrega Pendiente',
                       PURCHASE_DELIVERY_IN_PROGRESS: 'Entrega en proceso',
                       PURCHASE_DELIVERED: 'Entrega Realizada'}

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
        self.mongo = kwargs.get('mongo')
        self.firebase = kwargs.get('firebase')

    def get_firebase(self):
        return self.firebase

    def get_mongo(self):
        return self.mongo

    def get_logger(self):
        return self.logger

    def get(self, product_id):
        try:
            # Authentication
            auth_header = request.headers.get('Authorization')
            auth_token = auth_header.split(" ")[TOKEN]
            firebase = self.get_firebase()
            auth = firebase.auth()
            user = auth.refresh(auth_token)

            mongo = self.get_mongo()
            purchases_cursor = mongo.db.purchases.find({"product_id": product_id})

            product = mongo.db.products.find_one({'_id': ObjectId(product_id)})

            purchases = []
            for purchase in purchases_cursor:
                self.logger.info(purchase)
                purchase_to_display = {}
                purchase_to_display ['product_name'] = product ['name']
                purchase_to_display ['units'] = purchase ['units']
                purchase_to_display ['currency'] = purchase ['currency']
                purchase_to_display ['value'] = purchase ['value']
                purchase_to_display ['_id'] = str(purchase ['_id'])
                purchases.append(purchase_to_display)

            response_data = purchases
            response = responsehandler.ResponseHandler(status.HTTP_200_OK, response_data)
            response.add_autentication_header(user['refreshToken'])
            return response.get_response()

        except IndexError as e:
            error = errorhandler.ErrorHandler(status.HTTP_401_UNAUTHORIZED, 'Debe autenticarse previamente.')
            return error.get_error_response()

        except AttributeError as e:
            error = errorhandler.ErrorHandler(status.HTTP_401_UNAUTHORIZED, 'Debe autenticarse previamente.')
            return error.get_error_response()

        except pyrebase.pyrebase.HTTPError as e:
            error_message = errorhandler.get_error_message(e)
            error = errorhandler.ErrorHandler(status.HTTP_400_BAD_REQUEST, error_message)
            return error.get_error_response()

        except pymongo.errors.PyMongoError as e:
            self.logger.info(e)
            error = errorhandler.ErrorHandler(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Surgió un problema al acceder a la base de datos')
            return error.get_error_response()

        except Exception as e:
            self.logger.info(e)
            error = errorhandler.ErrorHandler(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Surgió un problema inesperado')
            return error.get_error_response()

    def post(self, product_id):
        try:
            # Authentication
            auth_header = request.headers.get('Authorization')
            auth_token = auth_header.split(" ")[TOKEN]
            firebase = self.get_firebase()
            auth = firebase.auth()
            user = auth.refresh(auth_token)

            json_data = request.get_json(force=True)
            units = json_data['units']

            mongo = self.get_mongo()
            product = mongo.db.products.find_one({'_id': ObjectId(product_id)})
            self.logger.info('product : %s', product)

            available_units = product ['units']
            if available_units < units:
                error = errorhandler.ErrorHandler(status.HTTP_409_CONFLICT, 'No hay disponibilidad de las unidades solicitadas.')
                return error.get_error_response()

            product_availability = {'units': (available_units - units)}
            mongo.db.products.update_one({'_id': ObjectId(product_id)}, {'$set': product_availability})

            purchase = {}
            purchase ['product_id'] = str(product ['_id'])
            purchase ['user_id'] = user ['userId']
            purchase ['units'] = units
            purchase ['currency'] = product ['currency']
            purchase ['value'] = units * product ['price']
            purchase['month_created'] = datetime.datetime.now().strftime("%b")

            purchase_id = mongo.db.purchases.insert_one(purchase).inserted_id
            
            seller = product['user_id']
            buyer = user ['userId']
            
            mongo.db.users.update_one({'uid': seller}, {'$push': {"ventas": str(purchase_id)}})
            mongo.db.users.update_one({'uid': buyer}, {'$push': {"compras": str(purchase_id)}})
            

            response_data = {'purchase_id': str(purchase_id)}
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

    @classmethod
    def get_purchase_state(self, state_str):
        for state_key, state_val in self.PURCHASE_STATES.items():
            if state_str == state_val:
                return state_key
        raise InvalidStateException