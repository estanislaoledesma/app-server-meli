# coding: utf-8
from flask_restful import Resource
from flask import request, redirect, url_for, jsonify
from ..settings import errorhandler, responsehandler
from flask_api import status
import pyrebase, pymongo
import base64
from gridfs import GridFS
from bson import ObjectId
from flask_restful import reqparse
from .deliveries import getDistance
import sys

TOKEN = 1
THUMBNAIL = 0


class Search(Resource):

    DISTANCE_RATIO = 5
    MIN_PRICE = 0
    MAX_PRICE = sys.maxsize

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
        self.mongo = kwargs.get('mongo')
        self.firebase = kwargs.get('firebase')
        self.fs = GridFS(self.mongo.db)

    def get(self):
        try:
            # Authentication
            auth_header = request.headers.get('Authorization')
            auth_token = auth_header.split(" ")[TOKEN]
            auth = self.firebase.auth()
            user = auth.refresh(auth_token)

            parser = reqparse.RequestParser()
            parser.add_argument('name')
            parser.add_argument('description')
            parser.add_argument('latitude')
            parser.add_argument('longitude')
            parser.add_argument('lowest_price')
            parser.add_argument('greatest_price')
            parser.add_argument('category')
            args = parser.parse_args()
            search_name = args ['name']
            search_description = args ['description']
            search_latitude = args ['latitude']
            search_longitude = args['longitude']
            destination = [search_latitude, search_longitude]
            self.logger.info("destination: %s", str(destination))
            search_lowest_price = Search.MIN_PRICE
            search_greatest_price = Search.MAX_PRICE

            try:
                search_lowest_price = int(args['lowest_price'])
                search_greatest_price = int(args['greatest_price'])
            except ValueError as e:
                self.logger.info("No price range search")

            search_category = args ['category']


            products_cursor = self.mongo.db.products.find({'name': {'$regex': '.*' + search_name + '.*', '$options': 'i'},
                                                           'description': {'$regex': '.*' + search_description + '.*', '$options': 'i'},
                                                           'price': {'$gte': search_lowest_price, '$lte': search_greatest_price},
                                                           'category': {'$regex': '.*' + search_category + '.*', '$options': 'i'}})

            products = []
            for product in products_cursor:
                #TODO filter by location
                self.logger.info(product)
                product_to_display = {}
                product_to_display ['name'] = product ['name']
                product_to_display ['price'] = product ['price']
                if (product ['images']):
                    product_to_display ['thumbnail'] = self.encode_image(product ['images'] [THUMBNAIL])
                product_to_display ['_id'] = str(product ['_id'])

                user_data = self.mongo.db.users.find_one({"uid": user ['userId']})
                self.logger.info('user data : %s', user_data)
                product_to_display ['user_name'] = user_data['display_name']
                product_to_display ['user_rating'] = user_data['rating']

                productLocation = [product ['latitude'], product ['longitude']]
                if (destination [0] and getDistance(productLocation, destination) > Search.DISTANCE_RATIO):
                    continue
                products.append(product_to_display)

            products.sort(key = lambda product: product ['user_rating'], reverse=True)
            response_data = products
            response = responsehandler.ResponseHandler(status.HTTP_200_OK, response_data)
            response.add_autentication_header(user['refreshToken'])
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
            self.logger.info(e)
            error = errorhandler.ErrorHandler(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Surgió un problema al acceder a la base de datos')
            return error.get_error_response()


    def decoded_images(self, encoded_images, product_name):
        images = []
        i = 0
        for image in encoded_images:
            name = product_name + str(i)
            fs_id = self.fs.put(base64.b64decode(image), filename=name)
            images.append(name)
            i+=1

        return images

    def encode_image(self, image_name):
        image = self.fs.get_last_version(filename=image_name).read()
        return str(base64.b64encode(image), 'utf-8')
