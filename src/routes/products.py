# coding: utf-8
from flask_restful import Resource
from flask import request, redirect, url_for, jsonify
from ..settings import errorhandler, responsehandler
from flask_api import status
import pyrebase, pymongo
import base64
import os
from werkzeug.datastructures import FileStorage

class Products(Resource):

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
        self.mongo = kwargs.get('mongo')
        self.firebase = kwargs.get('firebase')
        self.photos = kwargs.get('photos')
        
    def get(self):
        try:
            # Authentication
            auth_header = request.headers.get('Authorization')
            auth_token = auth_header.split(" ")[1]
            auth = self.firebase.auth()
            user = auth.refresh(auth_token)

            products_cursor = self.mongo.db.products.find()
            products = {}
            for product in products_cursor:
                product_to_display = product
                product_to_display ['_id'] = str(product_to_display ['_id'])
                products [str(product ['_id'])] = product_to_display

            response_data = {'token': user['refreshToken'], 'products': products}
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
            error = errorhandler.ErrorHandler(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Surgió un problema al acceder a la base de datos')
            return error.get_error_response()

    def post(self):
        try:
            # Authentication
            auth_header = request.headers.get('Authorization')
            auth_token = auth_header.split(" ")[1]
            auth = self.firebase.auth()
            user = auth.refresh(auth_token)

            json_data = request.get_json(force=True)
            self.logger.info(json_data)
            product = json_data['product']

            product_to_publish = {}
            product_to_publish ['userId'] = user['userId']
            product_to_publish ['name'] = product['name']

#            product_to_publish ['images'] = product['images']
            self.save_images(product['images'])

            product_to_publish ['price'] = product['price']
            product_to_publish ['description'] = product['description']
            product_id = self.mongo.db.products.insert_one(product_to_publish).inserted_id
            product_to_publish ['_id'] = str(product_id)

            response_data = {'token': user['refreshToken'], 'product': product_to_publish}
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
            error = errorhandler.ErrorHandler(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Surgió un problema al acceder a la base de datos')
            return error.get_error_response()

    def save_images(self, images):
        for image in images:
            file = None
            with open("foo.jpg", "wb") as f:
                f.write(base64.b64decode(image))
                file = FileStorage(f)
            path = self.photos.save(file)

#            self.photos.save(base64.b64decode(image))

#            with open("foo.jpg", "wb") as f:
                #base64.b64decode(image)
                #base64.decodebytes(image)
#                f.write(base64.b64decode(image))

#            file = request.files['file']
#            file.save(os.path.join("/images/", "image.jpg"))
