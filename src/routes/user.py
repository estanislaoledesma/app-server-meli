import firebase_admin
from firebase_admin import auth
from flask_restful import Api, Resource
from flask import Response, request, jsonify, json, redirect, url_for
import pyrebase
from ..settings import application


class Sign_Up(Resource):

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')

    def post(self):
        json_data = request.get_json(force=True)
        email = json_data['email']
        password = json_data['password']
        display_name = json_data['display_name']
        
        try:
            user = auth.create_user(
                    email = email,
                    email_verified = False,
                    password = password,
                    display_name = display_name,
                    disabled = False)
            return Response('User created with uid: '+user.uid, status = 201, mimetype = 'text/html')
        except ValueError:
            return Response('Parametros faltantes/erroneos', status = 400, mimetype = 'text/html')
        except auth.AuthError:
            return Response('Error al generar el usuario', status = 500, mimetype = 'text/html')

 
class Login(Resource):
 
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
 
    def post(self):
        json_data = request.get_json(force=True)
        email = json_data['email']
        password = json_data['password']
        
        pyauth = application.firebase.auth()
        try:
            user = pyauth.sign_in_with_email_and_password(email, password)
        
        except pyrebase.pyrebase.HTTPError:
            body = json.dumps("Datos incorrectos. Try again")
            return Response(body, status=400, mimetype='application/json')

        body = json.dumps("Welcome back "+user['email']+'and token: '+user['idToken'])
#         return Response(body, status=200, mimetype='application/json')
        return redirect(url_for('hello'))
        

