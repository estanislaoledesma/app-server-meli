from flask_restful import Resource, Api
from flask import Response, json, jsonify

class HelloWorld(Resource):

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')

    def get(self):
        body = json.dumps("Hola Mundo")
        self.logger.info('Hola Mundo')
        response = Response(body, status = 200, mimetype = 'application/json')
        return response
