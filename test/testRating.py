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

class TestRating(TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.app.environ_base['HTTP_AUTHORIZATION'] = ' testToken'

    def tearDown(self):
        pass

    @patch('src.routes.rating.Rating.get_mongo')
    @patch('src.routes.rating.Rating.get_firebase')
    def test_put_ok(self, mock_get_firebase, mock_get_mongo):
        mockAux = MagicMock()
        mockAux.refresh.return_value = {'userId': 'userId', 'refreshToken': 'testToken'}
        mock_get_firebase.return_value = mockAux
        mockAux.auth.return_value = mockAux

        mockDB = MagicMock()

        p = PropertyMock(return_value = MagicMock())
        type(mockDB).users = p

        mockMongo = MagicMock()
        mock_get_mongo.return_value =  mockMongo
        type(mockMongo).db = PropertyMock(return_value = mockDB)

        new_rating = {"rating": 1}

        response = self.app.put('/users/5c06f868556f89598152f2eb/score', json = new_rating)
        assert status.is_success(response.status_code)

