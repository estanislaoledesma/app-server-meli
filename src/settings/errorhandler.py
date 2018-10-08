from flask import jsonify, make_response
import json

def get_error_message(error):
    error_json = error.args[1]
    error_message = json.loads(error_json)["error"]["message"]
    error_message = error_message.lower().replace("_", " ")
    return error_message

class ErrorHandler(object):

    def __init__(self, status_code, error):
        self.errorResponse = make_response(jsonify(description = error), status_code)

    def get_error_response(self):
        return self.errorResponse
