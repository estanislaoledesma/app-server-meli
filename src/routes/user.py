from flask_restful import Resource
from flask import request, redirect, url_for, jsonify
from ..settings import error_handler, response_handler
from ..settings import config
import pyrebase

class Sign_Up(Resource):

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
        self.firebase = kwargs.get('firebase')

    def post(self):

#        try:
            json_data = request.get_json(force=True)
            self.logger.info(json_data)
            email = json_data['email']
            password = json_data['password']
            self.logger.info(email)
            self.logger.info(password)

            auth = self.firebase.auth()
            user = auth.create_user_with_email_and_password(email, password)
            response_data = {'token': user ['idToken']}
            response = response_handler.Response_Handler(config.Config.CODE_OK, response_data)
            return response.getResponse()

#        except pyrebase.pyrebase.HTTPError:
#            error = error_handler.Error_Handler(config.Config.CODE_BAD_REQUEST, 'Datos incorrectos. Intente de nuevo.')
#            return error.getErrorResponse()

 
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
            response = response_handler.Response_Handler(config.Config.CODE_OK, response_data)
#           return response.getResponse()

        except pyrebase.HTTPError:
            error = error_handler.Error_Handler(config.Config.CODE_BAD_REQUEST, 'Datos incorrectos. Intente de nuevo.')
            return error.getErrorResponse()

        return redirect(url_for('hello'))
        

