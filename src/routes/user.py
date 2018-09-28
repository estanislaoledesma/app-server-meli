from flask_restful import Resource
from flask import request, redirect, url_for, jsonify
import json
from ..settings import error_handler, response_handler
import pyrebase
from flask_api import status

class Sign_Up(Resource):

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
        self.firebase = kwargs.get('firebase')

    def post(self):
        try:
            json_data = request.get_json(force=True)
            self.logger.info(json_data)
            email = json_data['email']
            password = json_data['password']
            self.logger.info(email)
            self.logger.info(password)

            auth = self.firebase.auth()
            user = auth.create_user_with_email_and_password(email, password)
            response_data = {'token': user ['idToken']}
            response = response_handler.Response_Handler(status.HTTP_200_OK, response_data)
            return response.getResponse()

        except pyrebase.pyrebase.HTTPError:
            error = error_handler.Error_Handler(status.HTTP_400_BAD_REQUEST, 'Datos incorrectos. Intente de nuevo.')
            return error.getErrorResponse()

 
class Login(Resource):
 
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
        self.firebase = kwargs.get('firebase')

    def post(self):
        json_data = request.get_json(force=True)
        email = json_data['email']
        password = json_data['password']
        
        auth = self.firebase.auth()
        try:
            user = auth.sign_in_with_email_and_password(email, password)

            response_data = {'token': user['idToken']}
            response = response_handler.Response_Handler(status.HTTP_200_OK, response_data)
            return response.getResponse()

        except pyrebase.pyrebase.HTTPError as e:
            error_json = e.args[1]
            error_message = json.loads(error_json)["error"]["message"]
            error = error_handler.Error_Handler(status.HTTP_400_BAD_REQUEST, error_message)
            return error.getErrorResponse()

        # return redirect(url_for('hello'))
        

