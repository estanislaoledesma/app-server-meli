from flask_restful import Resource
from flask import jsonify
from ..settings import config, response_handler

class HelloWorld(Resource):

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')

    def get(self):
        response_data = {'Hello': 'World'}
        response = response_handler.Response_Handler(config.Config.CODE_OK, response_data)
        return response.getResponse()