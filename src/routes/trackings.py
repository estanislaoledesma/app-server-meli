# coding: utf-8
from flask_restful import Resource
from flask import request
from ..settings import errorhandler, responsehandler
from flask_api import status
import pyrebase, pymongo, requests
from bson.objectid import ObjectId
from . import purchases

TOKEN = 1

class Deliveries(Resource):

    TRACKING_URL = "http://localhost:8080/tracking/"

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
        self.mongo = kwargs.get('mongo')
        self.firebase = kwargs.get('firebase')
        self.gmaps = kwargs.get('gmaps')

    def get(self, purchase_id):
        try:
            # Authentication
            auth_header = request.headers.get('Authorization')
            auth_token = auth_header.split(" ")[TOKEN]
            auth = self.firebase.auth()
            user = auth.refresh(auth_token)

            purchase = self.mongo.db.purchases.find_one({'_id': ObjectId(purchase_id)})
            self.logger.info('purchase : %s', purchase)

            purchase_state = purchase ['state']
            if (purchase_state < purchases.Purchases.PURCHASE_CHECKOUT_DELIVERY):
                error = errorhandler.ErrorHandler(status.HTTP_409_CONFLICT, 'No se estableció una entrega aún.')
                return error.get_error_response()

            delivery_id = purchase ['delivery_id']

            tracking = {}
            tracking ['id'] = delivery_id
            tracking ['status'] = ''
            tracking ['updateAt'] = 0

            response = requests.post(url = self.TRACKING_URL + str(delivery_id), params=tracking)

            if response.status_code != status.HTTP_200_OK:
                error_message = response.reason
                error = errorhandler.ErrorHandler(status.HTTP_503_SERVICE_UNAVAILABLE, error_message)
                return error.get_error_response()

            response_data = response.json()

            purchase_update = {'status': response_data ['status']}
            self.mongo.db.purchases.update_one({'_id': ObjectId(purchase_id)}, {'$set': purchase_update})

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