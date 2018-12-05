# coding: utf-8
from flask_restful import Resource
from flask import request
from ..settings import errorhandler, responsehandler
from flask_api import status
import pyrebase, pymongo, requests
from ..models import push
from bson.objectid import ObjectId
from . import purchases

TOKEN = 1

class Payments(Resource):

    PENDING_PAYMENT_PROCESS = 2
    PAYMENT_ACCEPTED = 3
    PAYMENT_REJECTED = 4

    PAYMENT_STATUS = {PENDING_PAYMENT_PROCESS: 'Pago pendiente de proceso',
                       PAYMENT_ACCEPTED: 'Pago Aceptado',
                       PAYMENT_REJECTED: 'Pago Rechazado'}

    PAYEMENTS_URL = "http://melisharedserver.herokuapp.com/payment"

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

    def post(self, purchase_id):
        try:
            # Authentication
            auth_header = request.headers.get('Authorization')
            auth_token = auth_header.split(" ")[TOKEN]
            firebase = self.get_firebase()
            auth = firebase.auth()
            user = auth.refresh(auth_token)

            json_data = request.get_json(force=True)
            method = json_data ['payment_method']
            card_number = json_data ['card_number']
            card_cvc = json_data['card_cvc']
            card_expiration_year = json_data['card_expiration_year']
            card_expiration_month = json_data['card_expiration_month']
            card_holder = json_data['card_holder']

            mongo = self.get_mongo()
            purchase = mongo.db.purchases.find_one({'_id': ObjectId(purchase_id)})
            self.logger.info('purchase : %s', purchase)

            payment_method = {}
            payment_method ['expiration_month'] = card_expiration_month
            payment_method ['expiration_year'] = card_expiration_year
            payment_method ['method'] = method
            payment_method ['number'] = card_number
            payment_method ['type'] = method

            payment = {}
            payment ['currency'] = purchase ['currency']
            payment ['value'] = purchase ['value']
            payment ['paymentMethod'] = payment_method
            payment ['status'] = Payments.PAYMENT_STATUS [Payments.PENDING_PAYMENT_PROCESS]

            payment_id = mongo.db.payments.insert_one(payment).inserted_id

            payment ['transaction_id'] = str(payment_id)
            payment.pop('_id', None)
            self.logger.info('payment : %s', payment)

            response = requests.post(url = self.PAYEMENTS_URL, json = payment)

            if response.status_code != status.HTTP_201_CREATED:
                error_message = response.content
                error = errorhandler.ErrorHandler(status.HTTP_503_SERVICE_UNAVAILABLE, error_message)
                return error.get_error_response()

            purchase_update = {'payment_id': str(payment_id)}
            mongo.db.purchases.update_one({'_id': ObjectId(purchase_id)}, {'$set': purchase_update})

            response_data = {'payment_id': str(payment_id)}
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
            firebase = self.get_firebase()
            auth = firebase.auth()
            user = auth.refresh(auth_token)

            mongo = self.get_mongo()
            purchase = mongo.db.purchases.find_one({'_id': ObjectId(purchase_id)})
            self.logger.info('purchase : %s', purchase)

            payment = mongo.db.payments.find_one({'_id': ObjectId(purchase ['payment_id'])})
            self.logger.info('payment : %s', payment)

            payment ['_id'] = str(payment ['_id'])

            response_data = payment
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

class PaymentStatus(Resource):

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

    def put(self, payment_id):
        try:
            json_data = request.get_json(force=True)
            self.logger.info('edit payment: %s', json_data)
            new_status = json_data ['status']
            tracking_id = json_data ['tracking_id']

            mongo = self.get_mongo()
            mongo.db.payments.update_one({"_id": ObjectId(payment_id)}, {'$set': {'status': new_status}})

            purchase = mongo.db.purchases.find_one({'payment_id': payment_id})
            self.logger.info('purchase : %s', purchase)

            delivery_id = purchase ['delivery_id']

            mongo.db.deliveries.update_one({"_id": ObjectId(delivery_id)}, {'$set': {'tracking_id': tracking_id}})

            purchase = mongo.db.purchases.find_one({'payment_id': payment_id})
            user_id = str(purchase['user_id'])

            user = mongo.db.users.find_one({'uid': user_id})
            self.logger.info('user : %s', user)
            registration_id = user['registration_id']

            message = 'El estado de su pago ahora es: ' + new_status
            push.sendPushNotification(registration_id, 'Actualización de estado de compra', message)

            response_data = {}
            response = responsehandler.ResponseHandler(status.HTTP_200_OK, response_data)
            return response.get_response()

        except ValueError as e:
            error = errorhandler.ErrorHandler(status.HTTP_400_BAD_REQUEST, 'Bad info')
            return error.get_error_response()


