import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_api import status

from unittest import TestCase
from mock import patch, MagicMock, PropertyMock

sys.modules['pyrebase'] = MagicMock()
sys.modules['flask_pymongo'] = MagicMock()
sys.modules['requests'] = MagicMock()
sys.modules['gridfs'] = MagicMock()
from src.settings.application import app

class TestSearch(TestCase):

    PRODUCTS = [
                    {"_id": "5c06f868556f89598152f2ec",
                     "name": "Producto Test1",
                     "description": "Producto de prueba",
                     "images": "",
                     "price": 50,
                     "category": "Categoría Test",
                     "ubication": "Ubicación Test",
                     "latitude": "-34.583540",
                     "longitude": "-58.406081",
                     "units": 1,
                     "user_id": "5c06f868556f89598152f2eb"},
                    {"_id": "5c06f868556f89598152f2eb",
                     "name": "Producto Test2",
                     "description": "Producto de prueba",
                     "images": "",
                     "price": 50,
                     "category": "Categoría Test",
                     "ubication": "Ubicación Test",
                     "latitude": "-34.583540",
                     "longitude": "-58.406081",
                     "units": 1,
                     "user_id": "5c06f868556f89598152f2eb"}
                ]
    USER = {'display_name': 'display_name',
            'email': 'email',
            'password': 'password',
            'phone': 'phone',
            'registration_id': 'registration_id',
            'rating': 1}

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.app.environ_base['HTTP_AUTHORIZATION'] = ' testToken'

    def tearDown(self):
        pass

    @patch('src.routes.search.Search.get_mongo')
    @patch('src.routes.search.Search.get_firebase')
    def test_get_ok(self, mock_get_firebase, mock_get_mongo):
        mockAux = MagicMock()
        mockAux.refresh.return_value = {'refreshToken': 'testToken', 'userId': 'userId'}
        mock_get_firebase.return_value = mockAux
        mockAux.auth.return_value = mockAux

        mockProducts = MagicMock()
        mockProducts.find.return_value = TestSearch.PRODUCTS

        mockDB = MagicMock()
        p = PropertyMock(return_value = mockProducts)
        type(mockDB).products = p

        mockUsers = MagicMock()
        mockUsers.find_one.return_value = TestSearch.USER

        p1 = PropertyMock(return_value = mockUsers)
        type(mockDB).users = p1

        mockMongo = MagicMock()
        mock_get_mongo.return_value =  mockMongo
        type(mockMongo).db = PropertyMock(return_value = mockDB)

        response = self.app.get('http://127.0.0.1:8000/products/search?name=rod&description=prue&latitude=-34.583540&longitude=-58.406081&lowest_price=49&greatest_price=50&category=ate')
        assert status.is_success(response.status_code)