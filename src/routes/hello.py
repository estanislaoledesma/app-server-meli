from flask_restful import Resource, Api
from flask import Response

class HelloWorld(Resource):

    def get(self):
        response = Response("Hola Mundo", status = 200, mimetype = 'application/json')
        return response
