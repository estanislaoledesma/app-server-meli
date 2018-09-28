from flask_restful import Resource
from flask import jsonify
from ..settings import responsehandler
from flask_api import status

class HelloWorld(Resource):

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')

    def get(self):
        response_data = {'Hello': 'World'}
        response = responsehandler.ResponseHandler(status.HTTP_200_OK, response_data)
        return response.get_response()