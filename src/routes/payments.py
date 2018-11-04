# coding: utf-8
from flask_restful import Resource
from flask import request
from ..settings import errorhandler, responsehandler
from flask_api import status
import pyrebase, pymongo
from bson.objectid import ObjectId
from . import purchases

TOKEN = 1

class Payments(Resource):

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
            payment_method = json_data ['payment_method']
            card_number = json_data ['card_number']
            card_cvc = json_data['card_cvc']
            card_expiry_date = json_data['card_expiry_date']
            card_holder = json_data['card_holder']

            purchase = self.mongo.db.purchases.find_one({'_id': ObjectId(purchase_id)})
            self.logger.info('purchase : %s', purchase)

            purchase_state = purchase ['state']
            if (purchase_state > purchases.Purchases.PURCHASE_CHECKOUT):
                error = errorhandler.ErrorHandler(status.HTTP_409_CONFLICT, 'El pago de la compra ya fue realizado.')
                return error.get_error_response()

            payment = {}
            payment['purchase_id'] = purchase_id
            payment['payment_method'] = payment_method
            payment['card_number'] = card_number
            payment['card_cvc'] = card_cvc
            payment['card_expiry_date'] = card_expiry_date
            payment['card_holder'] = card_holder

            payment_id = self.mongo.db.payments.insert_one(payment).inserted_id

            purchase_update = {'state': purchases.Purchases.PURCHASE_PAYMENT, 'payment_id': str(payment_id)}
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