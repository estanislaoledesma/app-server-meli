# coding: utf-8
from flask_restful import Resource
from flask import request
from ..settings import errorhandler, responsehandler
from flask_api import status
import pyrebase, pymongo
from gridfs import GridFS
import base64
from bson.objectid import ObjectId

TOKEN = 1

class Product(Resource):

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
        self.mongo = kwargs.get('mongo')
        self.firebase = kwargs.get('firebase')
        self.fs = GridFS(self.mongo.db)

    def get_firebase(self):
        return self.firebase

    def get_mongo(self):
        return self.mongo

    def get_logger(self):
        return self.logger

    def get_fs(self):
        return self.fs

    def get(self, product_id):
        try:
            # Authentication
            auth_header = request.headers.get('Authorization')
            auth_token = auth_header.split(" ")[TOKEN]
            firebase = self.get_firebase()
            auth = firebase.auth()
            user = auth.refresh(auth_token)

            mongo = self.get_mongo()
            product = mongo.db.products.find_one({'_id': ObjectId(product_id)})
            self.logger.info('product : %s', product)

            product_to_display = {}
            product_to_display ['_id'] = str(product ['_id'])
            product_to_display ['name'] = product ['name']
            product_to_display ['description'] = product ['description']
            product_to_display ['price'] = product ['price']
#            product_to_display ['currency'] = product ['currency']
            product_to_display ['images'] = self.encode_images(product ['images'])
            product_to_display ['category'] = product ['category']
            product_to_display ['units'] = product ['units']

            self.logger.info('user : %s', user)
            user_data = mongo.db.users.find_one({"uid": user ['userId']})
            self.logger.info('user data : %s', user_data)
            product_to_display ['display_name'] = user_data ['display_name']
            product_to_display ['ubication'] = product ['ubication']
            product_to_display ['owner_id'] = product ['user_id']

            response_data = product_to_display
            response = responsehandler.ResponseHandler(status.HTTP_200_OK, response_data)
            response.add_autentication_header(user ['refreshToken'])
            return response.get_response()

        except IndexError as e:
            error = errorhandler.ErrorHandler(status.HTTP_401_UNAUTHORIZED, 'Debe autenticarse previamente.')
            return error.get_error_response()

        except pyrebase.pyrebase.HTTPError as e:
            error_message = errorhandler.get_error_message(e)
            error = errorhandler.ErrorHandler(status.HTTP_400_BAD_REQUEST, error_message)
            return error.get_error_response()

        except pymongo.errors.PyMongoError as e:
            error = errorhandler.ErrorHandler(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Surgió un problema inesperado')
            return error.get_error_response()

    def encode_images(self, images_name):
        l = []
        for name in images_name:
            l.append( self.encode_image(name) )
        return l

    def encode_image(self, image_name):
        fs = self.get_fs()
        image = fs.get_last_version(filename=image_name).read()
        return str(base64.b64encode(image), 'utf-8')
