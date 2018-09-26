from flask import jsonify, make_response

class Error_Handler(object):

    def __init__(self, status_code, description):
        self.errorResponse = make_response(jsonify(description = description), status_code)

    def getErrorResponse(self):
        return self.errorResponse