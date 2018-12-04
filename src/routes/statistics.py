# coding: utf-8
from flask_restful import Resource
from flask import request, redirect, url_for, jsonify
from ..settings import errorhandler, responsehandler
from bson.objectid import ObjectId
from flask_api import status
import pyrebase, pymongo


class Statistics(Resource):

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
        self.mongo = kwargs.get('mongo')
        self.firebase = kwargs.get('firebase')
        self.server_id = kwargs.get('server_id')

    def get(self):
        try:
            users = self.mongo.db.users.find()
            user_amount = users.count()

            products = self.mongo.db.products.find()
            product_amount = products.count()

            purchases = self.mongo.db.purchases.find()
            purchase_amount = purchases.count()

            server = self.mongo.db.servers.find_one({'_id': ObjectId(self.server_id)})
            self.logger.info('server : %s', server)
            created_time = server ['createdTime']

            response_data = {'registered_users': user_amount,
                             'products_for_sale': product_amount,
                             'purchase_amount': purchase_amount,
                             'created_time': created_time}
            response = responsehandler.ResponseHandler(status.HTTP_200_OK, response_data)
            return response.get_response()

        except Exception as e:
            self.logger.info(e)
            error = errorhandler.ErrorHandler(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Surgió un problema inesperado')
            return error.get_error_response()