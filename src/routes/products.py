# coding: utf-8
from flask_restful import Resource
from flask import request, redirect, url_for, jsonify
from ..settings import errorhandler, responsehandler
from flask_api import status
import pyrebase, pymongo
import base64
import datetime
from gridfs import GridFS
from bson import ObjectId

TOKEN = 1
THUMBNAIL = 0


class Products(Resource):
    CURRENCY = 'ARS'

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

    def get(self):
        try:
            # Authentication
            auth_header = request.headers.get('Authorization')
            auth_token = auth_header.split(" ")[TOKEN]
            firebase = self.get_firebase()
            auth = firebase.auth()
            user = auth.refresh(auth_token)

            mongo = self.get_mongo()
            products_cursor = self.mongo.db.products.find()

            products = []
            for product in products_cursor:
                self.logger.info(product)
                product_to_display = {}
                product_to_display['name'] = product['name']
                product_to_display['price'] = product['price']
                if (product ['images']):
                    product_to_display ['thumbnail'] = self.encode_image(product ['images'] [THUMBNAIL])
                product_to_display['_id'] = str(product['_id'])
                products.append(product_to_display)

            response_data = products
            response = responsehandler.ResponseHandler(status.HTTP_200_OK, response_data)
            response.add_autentication_header(user['refreshToken'])
            return response.get_response()


        except pyrebase.pyrebase.HTTPError as e:
            error_message = errorhandler.get_error_message(e)
            error = errorhandler.ErrorHandler(status.HTTP_400_BAD_REQUEST, error_message)
            return error.get_error_response()

        except pymongo.errors.PyMongoError as e:
            self.logger.info(e)
            error = errorhandler.ErrorHandler(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Surgió un problema al acceder a la base de datos')
            return error.get_error_response()

        except Exception as e:
            self.logger.info(e)
            error = errorhandler.ErrorHandler(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Surgió un problema inesperado')
            return error.get_error_response()

    def post(self):
        try:
            # Authentication
            auth_header = request.headers.get('Authorization')
            auth_token = auth_header.split(" ")[TOKEN]
            firebase = self.get_firebase()
            auth = firebase.auth()
            user = auth.refresh(auth_token)

            json_data = request.get_json(force=True)
            product = json_data['product']

            product_to_publish = {}

            product_to_publish ['name'] = product ['name']
            product_to_publish ['description'] = product ['description']
            product_to_publish ['images'] = self.decoded_images(product ['images'], product ['name'])
            product_to_publish ['price'] = product ['price']
            product_to_publish ['category'] = product ['category']
            product_to_publish ['ubication'] = product ['ubication']
            product_to_publish ['latitude'] = product ['latitude']
            product_to_publish ['longitude'] = product ['longitude']
            product_to_publish ['units'] = product ['units']
            product_to_publish ['user_id'] = user ['userId']
            product_to_publish ['currency'] = self.CURRENCY
            product_to_publish['month_created'] = datetime.datetime.now().strftime("%b")

            mongo = self.get_mongo()
            product_id = mongo.db.products.insert_one(product_to_publish).inserted_id
            product_to_publish ['_id'] = str(product_id)

            response = responsehandler.ResponseHandler(status.HTTP_200_OK, {})
            response.add_autentication_header(user ['refreshToken'])
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

#        except Exception as e:
#            error = errorhandler.ErrorHandler(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Surgió un problema inesperado')
#            return error.get_error_response()

    def decoded_images(self, encoded_images, product_name):
        images = []
        i = 0
        for image in encoded_images:
            name = product_name + str(i)
            fs = self.get_fs()
            fs_id = fs.put(base64.b64decode(image), filename=name)
            images.append(name)
            i+=1
        return images

    def encode_image(self, image_name):
        fs = self.get_fs()
        image = fs.get_last_version(filename=image_name).read()
        return str(base64.b64encode(image), 'utf-8')
