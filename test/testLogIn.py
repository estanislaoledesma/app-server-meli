import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_api import status

from unittest import TestCase
from mock import patch, MagicMock, PropertyMock

sys.modules['pyrebase'] = MagicMock()
from src.settings.application import app

class TestLogIn(TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    @patch('src.routes.user.Login.get_mongo')
    @patch('src.routes.user.Login.get_firebase')
    def test_post_ok(self, mock_get_firebase, mock_get_mongo):
        email = 'test@domain.com'
        password = 'password'
        registration_id = 'registration_id'
        log_in_json = {'email': email,
                        'password': password,
                        'registration_id': registration_id}

        mockAux = MagicMock()
        mockAux.sign_in_with_email_and_password.return_value = {'localId': 'testId', 'refreshToken': 'testToken'}
        mock_get_firebase.return_value = mockAux
        mockAux.auth.return_value = mockAux

        mockUsers = MagicMock()
        mockUsers.update_one.return_value = {'_id': "testId"}

        mockDB = MagicMock()
        p = PropertyMock(return_value = mockUsers)
        type(mockDB).users = p

        mockMongo = MagicMock()
        mock_get_mongo.return_value =  mockMongo
        type(mockMongo).db = PropertyMock(return_value = mockDB)

        response = self.app.post('/users/login', json = log_in_json)
        assert status.is_success(response.status_code)
