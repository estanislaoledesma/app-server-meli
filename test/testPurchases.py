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

class TestPurchases(TestCase):

    PURCHASES = [
                    {
                        "_id": "5c06f91b556f895982990e97",
                        "currency": "ARS",
                        "product_name": "Producto Test1",
                        "units": 2,
                        "value": 50
                    },
                    {
                        "_id": "5c06f91b556f895982990e96",
                        "currency": "ARS",
                        "product_name": "Producto Test2",
                        "units": 1,
                        "value": 60
                    }
                ]
    PRODUCT = {"_id": "5c06f868556f89598152f2eb",
               "name": "Producto Test",
               "description": "Producto de prueba",
               "images": "",
               "price": 50,
               "category": "Categoría Test",
               "ubication": "Ubicación Test",
               "latitude": "-34.583540",
               "longitude": "-58.406081",
               "units": 1,
               "currency": "ARS",
               "user_id": "5c06f868556f89598152f2eb"}

    PRODUCT_UNAVAILABLE = {"_id": "5c06f868556f89598152f2eb",
                           "name": "Producto Test",
                           "description": "Producto de prueba",
                           "images": "",
                           "price": 50,
                           "category": "Categoría Test",
                           "ubication": "Ubicación Test",
                           "latitude": "-34.583540",
                           "longitude": "-58.406081",
                           "units": 0,
                           "currency": "ARS",
                           "user_id": "5c06f868556f89598152f2eb"}

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.app.environ_base['HTTP_AUTHORIZATION'] = ' testToken'

    def tearDown(self):
        pass

    @patch('src.routes.purchases.Purchases.get_mongo')
    @patch('src.routes.purchases.Purchases.get_firebase')
    def test_get_ok(self, mock_get_firebase, mock_get_mongo):
        mockAux = MagicMock()
        mockAux.refresh.return_value = {'userId': 'userId', 'refreshToken': 'testToken'}
        mock_get_firebase.return_value = mockAux
        mockAux.auth.return_value = mockAux

        mockPurchases = MagicMock()
        mockPurchases.find.return_value = TestPurchases.PURCHASES

        mockDB = MagicMock()
        p = PropertyMock(return_value = mockPurchases)
        type(mockDB).purchases = p

        mockMongo = MagicMock()
        mock_get_mongo.return_value =  mockMongo
        type(mockMongo).db = PropertyMock(return_value = mockDB)

        mockProducts = MagicMock()
        mockProducts.find_one.return_value = TestPurchases.PRODUCT

        p2 = PropertyMock(return_value = mockProducts)
        type(mockDB).products = p2

        response = self.app.get('/products/5c06f868556f89598152f2eb/purchases')
        assert status.is_success(response.status_code)

    @patch('src.routes.purchases.Purchases.get_mongo')
    @patch('src.routes.purchases.Purchases.get_firebase')
    def test_post_ok(self, mock_get_firebase, mock_get_mongo):
        mockAux = MagicMock()
        mockAux.refresh.return_value = {'userId': 'userId', 'refreshToken': 'testToken'}
        mock_get_firebase.return_value = mockAux
        mockAux.auth.return_value = mockAux

        mockPurchase = MagicMock()
        p0 = PropertyMock(return_value = "insertedId")
        type(mockPurchase).inserted_id = p0

        mockPurchases = MagicMock()
        mockPurchases.insert_one.return_value = mockPurchase

        mockDB = MagicMock()
        p = PropertyMock(return_value = mockPurchases)
        type(mockDB).users = p

        mockMongo = MagicMock()
        mock_get_mongo.return_value =  mockMongo
        type(mockMongo).db = PropertyMock(return_value = mockDB)

        mockProducts = MagicMock()
        mockProducts.find_one.return_value = TestPurchases.PRODUCT

        p2 = PropertyMock(return_value = mockProducts)
        type(mockDB).products = p2

        response = self.app.post('/products/5c06f868556f89598152f2eb/purchases', json = {"units": 1})
        assert status.is_success(response.status_code)

    @patch('src.routes.purchases.Purchases.get_mongo')
    @patch('src.routes.purchases.Purchases.get_firebase')
    def test_post_no_ok(self, mock_get_firebase, mock_get_mongo):
        mockAux = MagicMock()
        mockAux.refresh.return_value = {'userId': 'userId', 'refreshToken': 'testToken'}
        mock_get_firebase.return_value = mockAux
        mockAux.auth.return_value = mockAux

        mockPurchase = MagicMock()
        p0 = PropertyMock(return_value = "insertedId")
        type(mockPurchase).inserted_id = p0

        mockPurchases = MagicMock()
        mockPurchases.insert_one.return_value = mockPurchase

        mockDB = MagicMock()
        p = PropertyMock(return_value = mockPurchases)
        type(mockDB).users = p

        mockMongo = MagicMock()
        mock_get_mongo.return_value =  mockMongo
        type(mockMongo).db = PropertyMock(return_value = mockDB)

        mockProducts = MagicMock()
        mockProducts.find_one.return_value = TestPurchases.PRODUCT_UNAVAILABLE

        p2 = PropertyMock(return_value = mockProducts)
        type(mockDB).products = p2

        response = self.app.post('/products/5c06f868556f89598152f2eb/purchases', json = {"units": 1})
        assert status.is_client_error(response.status_code)
