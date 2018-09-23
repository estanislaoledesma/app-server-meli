
class Config(object):

    FB_CREDENTIALS = 'src/settings/credentials/meli-4620b-firebase-adminsdk-8c1z7-b12f7ba600.json'
    setup = {
        "apiKey": "AIzaSyD3s0dTCy3J4v_3FitnlF_K2qTzsevIIBg",
        "authDomain": "meli-4620b.firebaseapp.com",
        "databaseURL": "https://meli-4620b.firebaseio.com",
        "storageBucket": "meli-4620b.appspot.com",
        "serviceAccount": 'src/settings/credentials/meli-4620b-firebase-adminsdk-8c1z7-b12f7ba600.json'
    }
    CODE_OK = 200
    CODE_BAD_REQUEST = 400
    CODE_UNAUTHORIZED = 401
    CODE_NOT_FOUND = 404
    CODE_INTERNAL_SERVER_ERROR = 500

    def get_fb_credentials(self):
        return self.FB_CREDENTIALS
    
    def get_websetup(self):
        return self.setup

    def get_code_ok(self):
        return self.CODE_OK

    def get_code_bad_request(self):
        return self.CODE_BAD_REQUEST

    def get_code_unauthorized(self):
        return self.CODE_UNAUTHORIZED

    def get_code_not_foun(self):
        return self.CODE_NOT_FOUND

    def get_code_internal_server_error(self):
        return self.CODE_INTERNAL_SERVER_ERROR