# coding: utf-8
from bson import ObjectId
from flask_restful import Resource
from flask import request, redirect, url_for, jsonify
from ..settings import errorhandler, responsehandler
import pyrebase
from flask_api import status

TOKEN = 1

class SignUp(Resource):

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
        self.firebase = kwargs.get('firebase')
        self.mongo = kwargs.get('mongo')

    def post(self):
        json_data = request.get_json(force=True)
        try:
            email = json_data['email']
            password = json_data['password']
            display_name = json_data['display_name']
            address = json_data['address']
            city = json_data['city']
            phone = json_data['phone']
            
            if "" in [email, password, display_name,
                      address, city, phone]:
                raise ValueError
                
            
        except KeyError as e:
            error = errorhandler.ErrorHandler(status.HTTP_400_BAD_REQUEST, 'Bad info')
            return error.get_error_response()
            
        except ValueError as e:
            error = errorhandler.ErrorHandler(status.HTTP_400_BAD_REQUEST, 'You must input all data')
            return error.get_error_response()
        
        firebase = self.get_firebase()

        auth = firebase.auth()
        try:
            user = auth.create_user_with_email_and_password(email, password)

            user_data = {}
            user_data['email'] = email
            user_data['display_name'] = display_name
            user_data['address'] = address
            user_data['city'] = city
            user_data['phone'] = phone
#             user_data['profile_pic'] = ""
            user_id = str(self.mongo.db.users.insert_one(user_data).inserted_id)

            response_data = {'user_id': user_id, 'name': display_name,
                             'token': user['refreshToken']}
            response = responsehandler.ResponseHandler(status.HTTP_200_OK, response_data)
            return response.get_response()
        
        except ValueError as e:
            error = errorhandler.ErrorHandler(status.HTTP_400_BAD_REQUEST, 'Bad info')
            return error.get_error_response()

        except Exception as e:
            error = errorhandler.ErrorHandler(status.HTTP_400_BAD_REQUEST, 'Bad info (prbably email exsts)')
            return error.get_error_response()

        except pyrebase.pyrebase.HTTPError as e:
            error_message = errorhandler.get_error_message(e)
            error = errorhandler.ErrorHandler(status.HTTP_400_BAD_REQUEST, e)
            return error.get_error_response()

#         except Exception as e:
#             error = errorhandler.ErrorHandler(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Surgió un problema inesperado')
#             return error.get_error_response()

    def get_firebase(self):
        return self.firebase


class Login(Resource):
 
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
        self.firebase = kwargs.get('firebase')

    def post(self):
        json_data = request.get_json(force=True)
        email = json_data['email']
        password = json_data['password']
        
        auth = self.get_firebase().auth()
        try:
            user = auth.sign_in_with_email_and_password(email, password)

            response_data = {'email': email, 'password': password, 'token': user['refreshToken']}
            response = responsehandler.ResponseHandler(status.HTTP_200_OK, response_data)
            return response.get_response()

        except pyrebase.pyrebase.HTTPError as e:
            error_message = errorhandler.get_error_message(e)
            error = errorhandler.ErrorHandler(status.HTTP_400_BAD_REQUEST, error_message)
            return error.get_error_response()
        
        except ValueError as e:
            error = errorhandler.ErrorHandler(status.HTTP_400_BAD_REQUEST, 'Bad info')
            return error.get_error_response()

#        except AuthError as e:
#            error = errorhandler.ErrorHandler(status.HTTP_400_BAD_REQUEST, 'Bad info')
#            return error.get_error_response()

        except Exception as e:
            error = errorhandler.ErrorHandler(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Surgió un problema inesperado')
            return error.get_error_response()

    def get_firebase(self):
        return self.firebase
    
class User(Resource):

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
        self.firebase = kwargs.get('firebase')
        self.mongo = kwargs.get('mongo')
        
    def get_firebase(self):
        return self.firebase

    def get(self, user_id):
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                raise IndexError
            auth_token = auth_header.split(" ")[TOKEN]
            auth = self.firebase.auth()
            user = auth.refresh(auth_token)
            
            req_user = self.mongo.db.users.find_one({'_id': ObjectId(user_id)})
            
            info = {}
            info['display name'] = req_user['display_name']
            info['email'] = req_user['email']
            info['address'] = req_user['address']
            info['city'] = req_user['city']
            info['phone'] = req_user['phone']
#             info['profile_pic']
            
            response_data = {'token': user['refreshToken'], 'user_info': info}
            response = responsehandler.ResponseHandler(status.HTTP_200_OK, response_data)
            return response.get_response()
        
        except ValueError as e:
            error = errorhandler.ErrorHandler(status.HTTP_400_BAD_REQUEST, 'Bad info')
            return error.get_error_response()
        
        except IndexError as e:
            error = errorhandler.ErrorHandler(status.HTTP_401_UNAUTHORIZED, 'Debe autenticarse previamente.')
            return error.get_error_response()
 
        except AttributeError as e:
            error = errorhandler.ErrorHandler(status.HTTP_401_UNAUTHORIZED, 'Debe autenticarse previamente.')
            return error.get_error_response()
 
        except pyrebase.pyrebase.HTTPError as e:
            error_message = errorhandler.get_error_message(e)
            error = errorhandler.ErrorHandler(status.HTTP_400_BAD_REQUEST, error_message)
            return error.get_error_response()
