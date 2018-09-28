from flask_restful import Resource
from flask import jsonify
from ..settings import response_handler
from flask_api import status

class HelloWorld(Resource):

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')

    def get(self):
        response_data = {'Hello': 'World'}
        response = response_handler.Response_Handler(status.HTTP_200_OK, response_data)
        return response.getResponse()