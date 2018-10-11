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

    def get(self, product_id):
        try:
            # Authentication
            auth_header = request.headers.get('Authorization')
            auth_token = auth_header.split(" ")[TOKEN]
            auth = self.firebase.auth()
            user = auth.refresh(auth_token)

            product = self.mongo.db.products.find_one({'_id': ObjectId(product_id)})

            product_to_display = {}
            product_to_display['_id'] = str(product['_id'])
            product_to_display['name'] = product['name']
            product_to_display['price'] = product['price']
            product_to_display['images'] = self.encode_images(product['images'])
            product_to_display['category'] = product['category']
            product_to_display['ubication'] = product['ubication']
            product_to_display['units'] = product['units']

            response_data = {'token': user['refreshToken'], 'product': product_to_display}
            response = responsehandler.ResponseHandler(status.HTTP_200_OK, response_data)
            return response.get_response()

        except IndexError as e:
            error = errorhandler.ErrorHandler(status.HTTP_401_UNAUTHORIZED, 'Debe autenticarse previamente.')
            return error.get_error_response()

#        except AttributeError as e:
#            error = errorhandler.ErrorHandler(status.HTTP_401_UNAUTHORIZED, 'Debe autenticarse previamente.')
#            return error.get_error_response()

#        except pyrebase.pyrebase.HTTPError as e:
#            error_message = errorhandler.get_error_message(e)
#            error = errorhandler.ErrorHandler(status.HTTP_400_BAD_REQUEST, error_message)
#            return error.get_error_response()

#        except pymongo.errors.PyMongoError as e:
#            error = errorhandler.ErrorHandler(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Surgió un problema al acceder a la base de datos')
#            return error.get_error_response()

    def encode_images(self, images_name):
        l = []
        for name in images_name:
            l.append( self.encode_image(name) )
        return l

    def encode_image(self, image_name):
        image = self.fs.get_last_version(filename=image_name).read()
        return str(base64.b64encode(image), 'utf-8')
