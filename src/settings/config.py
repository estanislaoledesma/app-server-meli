# coding: utf-8

class Config(object):

    FB_CREDENTIALS = 'src/settings/credentials/meli-4620b-firebase-adminsdk-8c1z7-b12f7ba600.json'
    setup = {
        "apiKey": "AIzaSyD3s0dTCy3J4v_3FitnlF_K2qTzsevIIBg",
        "authDomain": "meli-4620b.firebaseapp.com",
        "databaseURL": "https://meli-4620b.firebaseio.com",
        "storageBucket": "meli-4620b.appspot.com",
        "serviceAccount": 'src/settings/credentials/meli-4620b-firebase-adminsdk-8c1z7-b12f7ba600.json'
    }

    def get_fb_credentials(self):
        return self.FB_CREDENTIALS
    
    def get_websetup(self):
        return self.setup