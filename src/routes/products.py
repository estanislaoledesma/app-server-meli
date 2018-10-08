from flask_restful import Resource
from flask import request, redirect, url_for, jsonify
from ..settings import errorhandler, responsehandler
from flask_api import status
import pyrebase, pymongo

class Products(Resource):

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
        self.mongo = kwargs.get('mongo')
        self.firebase = kwargs.get('firebase')
        
    def get(self):
        try:
            # Authentication
            auth_header = request.headers.get('Authorization')
            auth_token = auth_header.split(" ")[1]
            auth = self.firebase.auth()
            user = auth.refresh(auth_token)

            products = self.mongo.db.products.find()
            response_data = {'token': user['refreshToken'], 'products': dict(products)}
            response = responsehandler.ResponseHandler(status.HTTP_200_OK, response_data)
            return response.get_response()

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

        except pymongo.errors.PyMongoError as e:
            error = errorhandler.ErrorHandler(status.HTTP_500_INTERNAL_SERVER_ERROR, e)
            return error.get_error_response()
    
    