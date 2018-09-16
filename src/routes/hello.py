from flask_restful import Resource, Api
from flask import Response, json, jsonify

class HelloWorld(Resource):

    def get(self):
        msg = json.dumps("Hola Mundo")
        response = Response(msg, status = 200, mimetype = 'application/json')
        return response
