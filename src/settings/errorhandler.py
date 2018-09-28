from flask import jsonify, make_response
import json


class ErrorHandler(object):

    def __init__(self, status_code, error):
        description = self.get_error_message(error)
        self.errorResponse = make_response(jsonify(description=description), status_code)

    def get_error_response(self):
        return self.errorResponse

    def get_error_message(self, error):
        error_json = error.args[1]
        error_message = json.loads(error_json)["error"]["message"]
        error_message = error_message.lower().replace("_", " ")
        return error_message
