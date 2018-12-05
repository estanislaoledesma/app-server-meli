import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_api import status

from unittest import TestCase
from mock import patch, MagicMock, PropertyMock

sys.modules['pyrebase'] = MagicMock()
from src.settings.application import app

class TestProduct(TestCase):

    PRODUCT = { "_id": "5c06f868556f89598152f2eb",
                "name": "Producto Test",
                "description": "Producto de prueba",
                "images": "",
                "price": 50,
                "category": "Categoría Test",
                "ubication": "Ubicación Test",
                "latitude": "-34.583540",
                "longitude": "-58.406081",
                "units": 1,
                "user_id": "5c06f868556f89598152f2eb"}

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.app.environ_base['HTTP_AUTHORIZATION'] = ' testToken'

    def tearDown(self):
        pass

    @patch('src.routes.product.Product.get_mongo')
    @patch('src.routes.product.Product.get_firebase')
    def test_get_ok(self, mock_get_firebase, mock_get_mongo):
        mockAux = MagicMock()
        mockAux.refresh.return_value = {'userId': 'userId', 'refreshToken': 'testToken'}
        mock_get_firebase.return_value = mockAux
        mockAux.auth.return_value = mockAux

        mockProduct = MagicMock()
        mockProduct.find_one.return_value = TestProduct.PRODUCT

        mockDB = MagicMock()
        p = PropertyMock(return_value = mockProduct)
        type(mockDB).products = p

        mockMongo = MagicMock()
        mock_get_mongo.return_value =  mockMongo
        type(mockMongo).db = PropertyMock(return_value = mockDB)

        response = self.app.get('/products/5c0700c7556f8960000b45e6')
        assert status.is_success(response.status_code)