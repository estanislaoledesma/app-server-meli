# coding: utf-8
from flask_restful import Resource
from flask import request, redirect, url_for, jsonify
from ..settings import errorhandler, responsehandler
from bson.objectid import ObjectId
from flask_api import status
import pyrebase, pymongo


class StatsUsers(Resource):

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
        self.mongo = kwargs.get('mongo')
        self.firebase = kwargs.get('firebase')
        self.server_id = kwargs.get('server_id')

    def get_firebase(self):
        return self.firebase

    def get_mongo(self):
        return self.mongo

    def get_logger(self):
        return self.logger

    def get(self):
        try:
            mongo = self.get_mongo()
            users = mongo.db.users.find()
            user_amount = users.count()
            
            response_data = {'total_users': user_amount,
                             'Jan': 0,
                             'Feb': 0,
                             'Mar': 0,
                             'Apr': 0,
                             'May': 0,
                             'Jun': 0,
                             'Jul': 0,
                             'Aug': 0,
                             'Sep': 0,
                             'Oct': 0,
                             'Nov': 0,
                             'Dec': 0
                             }
            
            for u in users:
                response_data[u['month_created']] += 1
            
            
            
            response = responsehandler.ResponseHandler(status.HTTP_200_OK, response_data)
            return response.get_response()

        except Exception as e:
            self.logger.info(e)
            error = errorhandler.ErrorHandler(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Surgió un problema inesperado')
            return error.get_error_response()
        
        
class StatsSales(Resource):

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
        self.mongo = kwargs.get('mongo')
        self.firebase = kwargs.get('firebase')
        self.server_id = kwargs.get('server_id')

    def get_firebase(self):
        return self.firebase

    def get_mongo(self):
        return self.mongo

    def get_logger(self):
        return self.logger

    def get(self):
        try:
            mongo = self.get_mongo()
            sales = mongo.db.purchases.find()
            sales_amount = sales.count()
            
            response_data = {'total_purchases': sales_amount,
                             'Jan': 0,
                             'Feb': 0,
                             'Mar': 0,
                             'Apr': 0,
                             'May': 0,
                             'Jun': 0,
                             'Jul': 0,
                             'Aug': 0,
                             'Sep': 0,
                             'Oct': 0,
                             'Nov': 0,
                             'Dec': 0
                             }
            
            for s in sales:
                response_data[s['month_created']] += 1
            
            
            
            response = responsehandler.ResponseHandler(status.HTTP_200_OK, response_data)
            return response.get_response()

        except Exception as e:
            self.logger.info(e)
            error = errorhandler.ErrorHandler(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Surgió un problema inesperado')
            return error.get_error_response()
        
        
class StatsProducts(Resource):

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
        self.mongo = kwargs.get('mongo')
        self.firebase = kwargs.get('firebase')
        self.server_id = kwargs.get('server_id')

    def get_firebase(self):
        return self.firebase

    def get_mongo(self):
        return self.mongo

    def get_logger(self):
        return self.logger

    def get(self):
        try:
            mongo = self.get_mongo()
            products = mongo.db.products.find()
            products_amount = products.count()
            
            response_data = {'total_products': products_amount,
                             'Jan': 0,
                             'Feb': 0,
                             'Mar': 0,
                             'Apr': 0,
                             'May': 0,
                             'Jun': 0,
                             'Jul': 0,
                             'Aug': 0,
                             'Sep': 0,
                             'Oct': 0,
                             'Nov': 0,
                             'Dec': 0
                             }
            
            for p in products:
                response_data[p['month_created']] += 1
            
            response = responsehandler.ResponseHandler(status.HTTP_200_OK, response_data)
            return response.get_response()

        except Exception as e:
            self.logger.info(e)
            error = errorhandler.ErrorHandler(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Surgió un problema inesperado')
            return error.get_error_response()
        
        
        
        
        
        