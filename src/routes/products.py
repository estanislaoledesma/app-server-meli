# coding: utf-8
from flask_restful import Resource
from flask import request, redirect, url_for, jsonify
from ..settings import errorhandler, responsehandler
from flask_api import status
import pyrebase, pymongo
import base64
from gridfs import GridFS
from bson import ObjectId

class Products(Resource):

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
        self.mongo = kwargs.get('mongo')
        self.firebase = kwargs.get('firebase')
        self.fs = GridFS(self.mongo.db)

    def get(self):
        try:
            # Authentication
            auth_header = request.headers.get('Authorization')
            auth_token = auth_header.split(" ")[1]
            auth = self.firebase.auth()
            user = auth.refresh(auth_token)

            products_cursor = self.mongo.db.products.find()
#            products = {}
            products = []
            for product in products_cursor:
                product_to_display = {}
                product_to_display['name'] = product['name']
                product_to_display['price'] = product['price']
                product_to_display['image'] = self.encode_image(product['images'][0])
                product_to_display['_id'] = str(product['_id'])

#                products[str(product['_id'])] = product_to_display
                products.append(product_to_display)

            response_data = {'token': user['refreshToken'], 'products': products}
            response = responsehandler.ResponseHandler(status.HTTP_200_OK, response_data)
            return response.get_response()

#        except IndexError as e:
#            error = errorhandler.ErrorHandler(status.HTTP_401_UNAUTHORIZED, 'Debe autenticarse previamente.')
#            return error.get_error_response()

#        except AttributeError as e:
#            error = errorhandler.ErrorHandler(status.HTTP_401_UNAUTHORIZED, 'Debe autenticarse previamente.')
#            return error.get_error_response()

        except pyrebase.pyrebase.HTTPError as e:
            error_message = errorhandler.get_error_message(e)
            error = errorhandler.ErrorHandler(status.HTTP_400_BAD_REQUEST, error_message)
            return error.get_error_response()

#        except pymongo.errors.PyMongoError as e:
#            error = errorhandler.ErrorHandler(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Surgió un problema al acceder a la base de datos')
#            return error.get_error_response()

    def encode_image(self, image_name):
        image = self.fs.get_last_version(filename=image_name).read()
        return base64.b64encode(image)



#            encoded_images = []
#        for name in images_name:
#            image = self.fs.get_last_version(name).read()
#            encoded_images.append(base64.b64encode(image))

#        return encoded_images

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
#            product_to_publish ['userId'] = user['userId']
            product_to_publish ['name'] = product['name']
            product_to_publish ['description'] = product['description']
#            product_to_publish ['images'] = product['images']
            product_to_publish['images'] = self.get_images(product['images'])
            product_to_publish ['price'] = product['price']

            product_id = self.mongo.db.products.insert_one(product_to_publish).inserted_id
            product_to_publish ['_id'] = str(product_id)

            response_data = {'token': user['refreshToken'], 'product': product_to_publish}
            response = responsehandler.ResponseHandler(status.HTTP_200_OK, response_data)
            return response.get_response()

#        except IndexError as e:
#            error = errorhandler.ErrorHandler(status.HTTP_401_UNAUTHORIZED, 'Debe autenticarse previamente.')
#            return error.get_error_response()

#        except AttributeError as e:
#            error = errorhandler.ErrorHandler(status.HTTP_401_UNAUTHORIZED, 'Debe autenticarse previamente.')
#            return error.get_error_response()

        except pyrebase.pyrebase.HTTPError as e:
            error_message = errorhandler.get_error_message(e)
            error = errorhandler.ErrorHandler(status.HTTP_400_BAD_REQUEST, error_message)
            return error.get_error_response()

        except pymongo.errors.PyMongoError as e:
            error = errorhandler.ErrorHandler(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Surgió un problema al acceder a la base de datos')
            return error.get_error_response()

    def get_images(self, encoded_images):
        images = []
        for image in encoded_images:
            name = 'foo.jpg'
            fs_id = self.fs.put(base64.b64decode(image), filename=name)
            images.append(name)

#            with open("foo.jpg", "wb") as f:
#                f.write(base64.b64decode(image))
#                fs_id = fs.put(f, content_type='image/jpg', file_name='foo.jpg')
#                images.append(fs_id)

        return images


#            with open("foo.jpg", "wb") as f:
                #base64.b64decode(image)
                #base64.decodebytes(image)
#                f.write(base64.b64decode(image))
