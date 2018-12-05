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

class TestUser(TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.app.environ_base['HTTP_AUTHORIZATION'] = ' testToken'

    def tearDown(self):
        pass

    @patch('src.routes.user.User.get_mongo')
    @patch('src.routes.user.User.get_firebase')
    def test_get_ok(self, mock_get_firebase, mock_get_mongo):
        mockAux = MagicMock()
        mockAux.refresh.return_value = {'refreshToken': 'testToken'}
        mock_get_firebase.return_value = mockAux
        mockAux.auth.return_value = mockAux

        mockUsers = MagicMock()
        mockUsers.find_one.return_value = {'_id': "testId"}

        mockDB = MagicMock()
        p = PropertyMock(return_value = mockUsers)
        type(mockDB).users = p

        mockMongo = MagicMock()
        mock_get_mongo.return_value =  mockMongo
        type(mockMongo).db = PropertyMock(return_value = mockDB)

        response = self.app.get('/users/user_id')
        assert status.is_success(response.status_code)

    @patch('src.routes.user.User.get_mongo')
    @patch('src.routes.user.User.get_firebase')
    def test_put_ok(self, mock_get_firebase, mock_get_mongo):
        mockAux = MagicMock()
        mockAux.refresh.return_value = {'refreshToken': 'testToken'}
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

        response = self.app.put('/users/user_id', json = {})
        assert status.is_success(response.status_code)
