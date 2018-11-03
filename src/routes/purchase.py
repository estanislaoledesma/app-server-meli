# coding: utf-8
from flask_restful import Resource
from flask import request
from ..settings import errorhandler, responsehandler
from flask_api import status
import pyrebase, pymongo
from bson.objectid import ObjectId

TOKEN = 1

class Purchase(Resource):

    PURCHASE_CHECKOUT = 0
    PURCHASE_PAYMENT = 2
    PURCHASE_CHECK_PAYMENT = 3
    PURCHASE_COMPLETED = 4

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
        self.mongo = kwargs.get('mongo')
        self.firebase = kwargs.get('firebase')

    def post(self, product_id):
        try:
            # Authentication
            auth_header = request.headers.get('Authorization')
            auth_token = auth_header.split(" ")[TOKEN]
            auth = self.firebase.auth()
            user = auth.refresh(auth_token)

            json_data = request.get_json(force=True)
            units = json_data['units']

            product = self.mongo.db.products.find_one({'_id': ObjectId(product_id)})
            self.logger.info('product : %s', product)

            available_units = product ['units']
            if available_units < units:
                error = errorhandler.ErrorHandler(status.HTTP_409_CONFLICT, 'No hay disponibilidad de las unidades solicitadas.')
                return error.get_error_response()

            product_availability = {'units': (available_units - units)}
            self.mongo.db.products.update_one({'_id': ObjectId(product_id)}, {'$set': product_availability})

            purchase = {}
            purchase['product_id'] = str(product['_id'])
            purchase['user_id'] = user['userId']
            purchase['units'] = units
            purchase['purchas_state'] = self.PURCHASE_CHECKOUT

            purchase_id = self.mongo.db.purchases.insert_one(purchase).inserted_id

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