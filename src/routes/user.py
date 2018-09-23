from flask_restful import Resource
from flask import request, redirect, url_for, jsonify
from ..settings import error_handler
from ..settings import config
import pyrebase

class Sign_Up(Resource):

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
        self.firebase = kwargs.get('firebase')

    def post(self):

        try:
            json_data = request.get_json(force=True)
            email = json_data['email']
            password = json_data['password']

            auth = self.firebase.auth()
            user = auth.create_user_with_email_and_password(email, password)
            return jsonify(code = config.Config.CODE_OK, token = user ['idToken'])

        except pyrebase.pyrebase.HTTPError:
            error = error_handler.Error_Handler(config.Config.CODE_BAD_REQUEST, 'Datos incorrectos. Intente de nuevo.')
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
            response = jsonify(code=config.Config.CODE_OK, token=user['idToken'])
#           return response

        except pyrebase.HTTPError:
            error = error_handler.Error_Handler(config.Config.CODE_BAD_REQUEST, 'Datos incorrectos. Intente de nuevo.')
            return error.getErrorResponse()

        return redirect(url_for('hello'))
        

