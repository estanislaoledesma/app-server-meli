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
        
    def get(self):
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                raise IndexError
            auth_token = auth_header.split(" ")[TOKEN]
            auth = self.firebase.auth()
            user = auth.refresh(auth_token)

            req_user = self.mongo.db.users.find_one({"uid": user ['userId']})
            self.logger.info('user : %s', req_user)

            compras = req_user['compras']
            
            compras_show = []
            
            for purchase_id in compras:
                purchase= self.mongo.db.purchases.find_one({"_id": ObjectId(purchase_id)})
                product = self.mongo.db.products.find_one({'_id': ObjectId(purchase ['product_id'])})
                seller = self.mongo.db.users.find_one({'uid': product['user_id']})
                
                self.logger.info(purchase)
                purchase_to_display = {}
                purchase_to_display['product_name'] = product ['name']
                purchase_to_display['units'] = purchase ['units']
                purchase_to_display['currency'] = purchase ['currency']
                purchase_to_display['value'] = purchase ['value']
                purchase_to_display['state'] = purchase ['state']
                purchase_to_display['username'] = seller['display_name']
                compras_show.append(purchase_to_display)

            
            response_data = compras_show
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
        
    def get(self):
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                raise IndexError
            auth_token = auth_header.split(" ")[TOKEN]
            auth = self.firebase.auth()
            user = auth.refresh(auth_token)

            req_user = self.mongo.db.users.find_one({"uid": user ['userId']})
            self.logger.info('user : %s', req_user)

            sales = req_user['ventas']
            
            sales_show = []
            
            for purchase_id in sales:
                purchase= self.mongo.db.purchases.find_one({"_id": ObjectId(purchase_id)})
                product = self.mongo.db.products.find_one({'_id': ObjectId(purchase ['product_id'])})
                buyer = self.mongo.db.users.find_one({'uid': purchase ['user_id']})
                
                self.logger.info(purchase)
                purchase_to_display = {}
                purchase_to_display['product_name'] = product ['name']
                purchase_to_display['units'] = purchase ['units']
                purchase_to_display['currency'] = purchase ['currency']
                purchase_to_display['value'] = purchase ['value']
                purchase_to_display['state'] = purchase ['state']
                purchase_to_display['username'] = buyer['display_name']
                sales_show.append(purchase_to_display)

            
            response_data = sales_show
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