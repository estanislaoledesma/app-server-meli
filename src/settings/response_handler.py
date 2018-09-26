from flask import jsonify, make_response

class Response_Handler(object):

    def __init__(self, status_code, data_dictionary):
        self.response = make_response(jsonify(data_dictionary), status_code)

    def getResponse(self):
        return self.response