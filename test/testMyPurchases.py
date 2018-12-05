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

class TestMyPurchases(TestCase):

    PURCHASES = [
                    {
                        "_id": "5c06f91b556f895982990e97",
                        "currency": "ARS",
                        "product_name": "Producto Test1",
                        "units": 2,
                        "value": 50,
                        "product_id": "5c06f91b556f895982990e96",
                    },
                    {
                        "_id": "5c06f91b556f895982990e96",
                        "currency": "ARS",
                        "product_name": "Producto Test2",
                        "units": 1,
                        "value": 60,
                        "product_id": "5c06f91b556f895982990e97",
                    }
                ]

    PRODUCT = {"_id": "5c06f868556f89598152f2ec",
                 "name": "Producto Test1",
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

    @patch('src.routes.activity.MyPurchases.get_mongo')
    @patch('src.routes.activity.MyPurchases.get_firebase')
    def test_get_ok(self, mock_get_firebase, mock_get_mongo):
        mockAux = MagicMock()
        mockAux.refresh.return_value = {'refreshToken': 'testToken', 'userId': 'userId'}
        mock_get_firebase.return_value = mockAux
        mockAux.auth.return_value = mockAux

        mockProducts = MagicMock()
        mockProducts.find_one.return_value = TestMyPurchases.PRODUCT

        mockDB = MagicMock()
        p = PropertyMock(return_value = mockProducts)
        type(mockDB).products = p

        mockPurchases = MagicMock()
        mockPurchases.find.return_value = TestMyPurchases.PURCHASES

        p1 = PropertyMock(return_value = mockPurchases)
        type(mockDB).purchases = p1

        mockMongo = MagicMock()
        mock_get_mongo.return_value =  mockMongo
        type(mockMongo).db = PropertyMock(return_value = mockDB)

        response = self.app.get('/mypurchases')
        assert status.is_success(response.status_code)