import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_api import status

from unittest import TestCase
from mock import patch, MagicMock, PropertyMock

sys.modules['pyrebase'] = MagicMock()
sys.modules['flask_pymongo'] = MagicMock()
sys.modules['requests'] = MagicMock()
from src.settings.application import app

class TestSignUp(TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    @patch('src.routes.user.SignUp.get_mongo')
    @patch('src.routes.user.SignUp.get_firebase')
    def test_post_ok(self, mock_get_firebase, mock_get_mongo):
        display_name = 'Test'
        email = 'test1@domain.com'
        password = 'password'
        phone = "phone"
        registration_id = "registration_id"
        sign_up_json = {'display_name': display_name,
                        'email': email,
                        'password': password,
                        'phone': phone,
                        'registration_id': registration_id}

        mockAux = MagicMock()
        mockAux.create_user_with_email_and_password.return_value = {'localId': 'testId', 'refreshToken': 'testToken'}
        mock_get_firebase.return_value = mockAux
        mockAux.auth.return_value = mockAux

        mockUser = MagicMock()
        id = PropertyMock(return_value = "inserted_id")
        type(mockUser).inserted_id = id

        mockUsers = MagicMock()
        mockUsers.insert_one.return_value = mockUser

        mockDB = MagicMock()
        p = PropertyMock(return_value=mockUsers)
        type(mockDB).users = p

        mockMongo = MagicMock()
        mock_get_mongo.return_value = mockMongo
        type(mockMongo).db = PropertyMock(return_value=mockDB)

        response = self.app.post('/users/signup', json = sign_up_json)
        assert status.is_success(response.status_code)
