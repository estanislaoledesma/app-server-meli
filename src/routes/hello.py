from flask_restful import Resource, Api
from flask import Response, json, jsonify

class HelloWorld(Resource):

    def get(self):
        body = json.dumps("Hola Mundo")
        response = Response(body, status = 200, mimetype = 'application/json')
        return response
