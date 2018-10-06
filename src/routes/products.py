from flask_restful import Resource
from flask import request, redirect, url_for, jsonify
from ..settings import errorhandler, responsehandler
from flask_api import status

class Publish(Resource):

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
        self.mongo = kwargs.get('mongo')
        
    def get(self):
        db_response = self.mongo.db.delete_one({'email': "foo@bar"})    
        response_data = {'Hello': 'World'}
        response = responsehandler.ResponseHandler(status.HTTP_200_OK, response_data)
        return response.get_response()
    
    