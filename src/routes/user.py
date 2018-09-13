import firebase_admin
from firebase_admin import auth
from flask_restful import Api, Resource
from flask import Response, request, jsonify

class Sign_Up(Resource):

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
            return Response(jsonify(user), status = 200, mimetype = 'application/json')
        except ValueError:
            return Response('Parametros faltantes/erroneos', status = 400, mimetype = 'text/html')
        except auth.AuthError:
            return Response('Error al generar el usuario', status = 500, mimetype = 'text/html')
