import firebase_admin
from firebase_admin import auth
from flask_restful import Api, Resource
from flask import Response, request, jsonify, json

class Sign_Up(Resource):

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')

    def post(self):
        try:
            json_data = request.get_json(force=True)
            email = json_data['email']
            password = json_data['password']
            display_name = json_data['display_name']
            user = auth.create_user(
                    email = email,
                    email_verified = False,
                    password = password,
                    display_name = display_name,
                    disabled = False)
#             body = json.dumps(user)
            return Response('User created with uid: '+user.uid, status = 200, mimetype = 'text/html')
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
        
        try:
            user = auth.get_user_by_email(email)
        except auth.AuthError:
            return Response('Error al obtener usuario', status = 500, mimetype = 'text/html')
        
        return Response('Bienvenido a MeLi '+email+'!', status = 200, mimetype = 'text/html')
        

