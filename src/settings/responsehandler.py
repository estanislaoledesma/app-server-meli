from flask import jsonify, make_response


class ResponseHandler(object):

    def __init__(self, status_code, data_dictionary):
        self.response = make_response(jsonify(data_dictionary), status_code)

    def get_response(self):
        return self.response
