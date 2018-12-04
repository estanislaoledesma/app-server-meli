# coding: utf-8
from flask_restful import Resource
from flask import request
from ..settings import errorhandler, responsehandler
from flask_api import status
import pyrebase, pymongo
from bson import ObjectId

TOKEN = 1

class Answers(Resource):

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')
        self.mongo = kwargs.get('mongo')
        self.firebase = kwargs.get('firebase')

    def get(self, question_id):
        try:
            # Authentication
            auth_header = request.headers.get('Authorization')
            auth_token = auth_header.split(" ")[TOKEN]
            auth = self.firebase.auth()
            user = auth.refresh(auth_token)

            answers_cursor = self.mongo.db.answers.find({'question_id': question_id})

            answers = []
            for answer in answers_cursor:
                self.logger.info(answer)
                answer_to_display = {}
                answer_to_display ['answer'] = answer ['answer']
                answer_to_display ['user_id'] = answer ['user_id']
                answer_to_display['_id'] = str(answer ['_id'])
                answers.append(answer_to_display)

            response_data = answers
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
            error = errorhandler.ErrorHandler(status.HTTP_500_INTERNAL_SERVER_ERROR,
                                              'Surgió un problema al acceder a la base de datos')
            return error.get_error_response()

        except Exception as e:
            self.logger.info(e)
            error = errorhandler.ErrorHandler(status.HTTP_500_INTERNAL_SERVER_ERROR, 'Surgió un problema inesperado')
            return error.get_error_response()

    def post(self, question_id):
        try:
            # Authentication
            auth_header = request.headers.get('Authorization')
            auth_token = auth_header.split(" ")[TOKEN]
            auth = self.firebase.auth()
            user = auth.refresh(auth_token)

#            question = self.mongo.db.questions.find_one({'_id': ObjectId(question_id)})
#            self.logger.info('question : %s', question)

            json_data = request.get_json(force=True)
            answer_str = json_data['answer']

            self.mongo.db.questions.update({'_id': ObjectId(question_id)}, {'$set': {'answer': answer_str}})

#            answer = {}
#            answer ['question_id'] = str(question_id)
#            answer ['user_id'] = user ['userId']
#            answer ['answer'] = answer_str

#            answer_id = self.mongo.db.answers.insert_one(answer).inserted_id
#            answer ['_id'] = str(answer_id)

#            response_data = answer
            response_data = {}
            response = responsehandler.ResponseHandler(status.HTTP_200_OK, response_data)
            response.add_autentication_header(user['refreshToken'])
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
