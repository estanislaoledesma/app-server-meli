from flask import jsonify

class Error_Handler(object):

    def __init__(self, code, description):
        self.errorResponse = jsonify(code = code, description = description)

    def getErrorResponse(self):
        return self.errorResponse