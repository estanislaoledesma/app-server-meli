# coding: utf-8
from bson import ObjectId
from flask_restful import Resource
from flask import request, redirect, url_for, jsonify
from ..settings import errorhandler, responsehandler
import pyrebase
from flask_api import status

TOKEN = 1

class MyPurchases(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
        self.firebase = kwargs.get('firebase')
        self.mongo = kwargs.get('mongo')

    def get_firebase(self):
        return self.firebase

    def get_mongo(self):
        return self.mongo

    def get_logger(self):
        return self.logger
        
    def get(self):
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                raise IndexError
            auth_token = auth_header.split(" ")[TOKEN]
            firebase = self.get_firebase()
            auth = firebase.auth()
            user = auth.refresh(auth_token)

            mongo = self.get_mongo()
            purchases_cursor = mongo.db.purchases.find({"user_id": user['userId']})
            self.logger.info('user : %s', purchases_cursor)
            
            purchases = []
            for purchase in purchases_cursor:
                product = mongo.db.products.find_one({"_id": ObjectId(purchase['product_id'])})
                self.logger.info(purchase)
                purchase_to_display = {}
                purchase_to_display['product_name'] = product['name']
                purchase_to_display['units'] = purchase['units']
                purchase_to_display['currency'] = purchase['currency']
                purchase_to_display['value'] = purchase['value']
                purchase_to_display['_id'] = str(purchase['_id'])
                purchases.append(purchase_to_display)
            
            response_data = purchases
            response = responsehandler.ResponseHandler(status.HTTP_200_OK, response_data)
            response.add_autentication_header(user['refreshToken'])
            return response.get_response()
        
        except ValueError as e:
            error = errorhandler.ErrorHandler(status.HTTP_400_BAD_REQUEST, 'Bad info')
            return error.get_error_response()
        
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

class MySales(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
        self.firebase = kwargs.get('firebase')
        self.mongo = kwargs.get('mongo')

    def get_firebase(self):
        return self.firebase

    def get_mongo(self):
        return self.mongo

    def get_logger(self):
        return self.logger

    def get(self):
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                raise IndexError
            auth_token = auth_header.split(" ")[TOKEN]
            firebase = self.get_firebase()
            auth = firebase.auth()
            user = auth.refresh(auth_token)

            mongo = self.get_mongo()
            products_cursor = mongo.db.products.find({"user_id": user['userId']})
            self.logger.info('user : %s', products_cursor)

            sales = []
            for product in products_cursor:
                purchases_cursor = mongo.db.purchases.find({"product_id": str(product['_id'])})
                self.logger.info(purchases_cursor)

                for purchase in purchases_cursor:
                    purchase_to_display = {}
                    purchase_to_display['product_name'] = product['name']
                    purchase_to_display['units'] = purchase['units']
                    purchase_to_display['currency'] = purchase['currency']
                    purchase_to_display['value'] = purchase['value']
                    purchase_to_display['_id'] = str(purchase['_id'])
                    sales.append(purchase_to_display)

            response_data = sales
            response = responsehandler.ResponseHandler(status.HTTP_200_OK, response_data)
            response.add_autentication_header(user['refreshToken'])
            return response.get_response()
        
        except ValueError as e:
            error = errorhandler.ErrorHandler(status.HTTP_400_BAD_REQUEST, 'Bad info')
            return error.get_error_response()
        
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