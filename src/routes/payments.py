# coding: utf-8
from flask_restful import Resource
from flask import request
from ..settings import errorhandler, responsehandler
from flask_api import status
import pyrebase, pymongo, requests
from bson.objectid import ObjectId
from . import purchases

TOKEN = 1

class Payments(Resource):

    PAYEMENTS_URL = "http://localhost:8080/payments"

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
        self.mongo = kwargs.get('mongo')
        self.firebase = kwargs.get('firebase')

    def post(self, purchase_id):
        try:
            # Authentication
            auth_header = request.headers.get('Authorization')
            auth_token = auth_header.split(" ")[TOKEN]
            auth = self.firebase.auth()
            user = auth.refresh(auth_token)

            json_data = request.get_json(force=True)
            method = json_data ['payment_method']
            card_number = json_data ['card_number']
            card_cvc = json_data['card_cvc']
            card_expiration_year = json_data['card_expiration_year']
            card_expiration_month = json_data['card_expiration_month']
            card_holder = json_data['card_holder']

            purchase = self.mongo.db.purchases.find_one({'_id': ObjectId(purchase_id)})
            self.logger.info('purchase : %s', purchase)

            purchase_state = purchase ['state']
            if (purchase_state > purchases.Purchases.PURCHASE_CHECKOUT_DELIVERY):
                error = errorhandler.ErrorHandler(status.HTTP_409_CONFLICT, 'El pago de la compra ya fue realizado.')
                return error.get_error_response()

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

            payment_id = self.mongo.db.payments.insert_one(payment).inserted_id

            payment ['transaction_id'] = str(payment_id)

            response = requests.post(url = self.PAYEMENTS_URL, params = payment)

            if response.status_code != status.HTTP_201_CREATED:
                error_message = response.reason
                error = errorhandler.ErrorHandler(status.HTTP_503_SERVICE_UNAVAILABLE, error_message)
                return error.get_error_response()

            purchase_update = {'state': purchases.Purchases.PURCHASE_PENDING_PAYMENT_PROCESS, 'payment_id': str(payment_id)}
            self.mongo.db.purchases.update_one({'_id': ObjectId(purchase_id)}, {'$set': purchase_update})

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