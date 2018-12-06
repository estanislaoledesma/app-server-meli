import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_api import status

from unittest import TestCase
from mock import patch, MagicMock, PropertyMock

sys.modules['pyrebase'] = MagicMock()
sys.modules['flask_pymongo'] = MagicMock()
from src.settings.application import app

class TestDeliveries(TestCase):

    DELIVERY = {
                    "_id": "5c0700c7556f8960000b45e6",
                    "cost": {
                        "currency": "ARS",
                        "value": 15.526744977904434
                    },
                    "distance": 1.0351163318602956,
                    "mail": "estanislaomledesma@gmail.com",
                    "purchaseQuantity": 1,
                    "status": "Entrega Realizada",
                    "tracking_id": "1000",
                    "userscore": 0,
                    "value": 50
                }

    PURCHASE = {
                    "_id": "5c06f91b556f895982990e97",
                    "currency": "ARS",
                    "product_name": "Producto Test1",
                    "units": 2,
                    "value": 50,
                    "payment_id": "5c06f91b556f895982990e97",
                    "product_id": "5c06f91b556f895982990e97",
                    "delivery_id": "5c06f91b556f895982990e97"
                }

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

    @patch('src.routes.deliveries.requests')
    @patch('src.routes.deliveries.Deliveries.get_mongo')
    @patch('src.routes.deliveries.Deliveries.get_firebase')
    def test_post_ok(self, mock_get_firebase, mock_get_mongo, mock_requests):
        mockAux = MagicMock()
        mockAux.refresh.return_value = {'userId': 'userId', 'refreshToken': 'testToken'}
        mock_get_firebase.return_value = mockAux
        mockAux.auth.return_value = mockAux

        mockUsers = MagicMock()
        mockUsers.find_one.return_value = {'userId': 'userId', 'email': 'email'}

        mockDB = MagicMock()
        p1 = PropertyMock(return_value = mockUsers)
        type(mockDB).users = p1

        mockProducts = MagicMock()
        mockProducts.find_one.return_value = TestDeliveries.PRODUCT

        mockDB = MagicMock()
        p2 = PropertyMock(return_value=mockProducts)
        type(mockDB).products = p2

        mockMongo = MagicMock()
        mock_get_mongo.return_value =  mockMongo
        type(mockMongo).db = PropertyMock(return_value = mockDB)

        mockPurchases = MagicMock()
        mockPurchases.find.return_value = mockPurchases
        mockPurchases.count.return_value = 5
        mockPurchases.find_one.return_value = TestDeliveries.PURCHASE

        p3 = PropertyMock(return_value = mockPurchases)
        type(mockDB).purchases = p3

        mockResponse = MagicMock()
        type(mockResponse).status_code = status.HTTP_200_OK
        mockResponse.json.return_value = {'cost': '5'}

        mock_requests.post.return_value = mockResponse

        new_delivery = {"destination_address": "Dirección Prueba",
                         "destination_latitude": "-34.592871",
                         "destination_longitude": "-58.406081"}

        response = self.app.post('/purchases/5c06f91b556f895982990e96/deliveries', json = new_delivery)
        assert status.is_success(response.status_code)

    @patch('src.routes.deliveries.requests')
    @patch('src.routes.deliveries.Deliveries.get_mongo')
    @patch('src.routes.deliveries.Deliveries.get_firebase')
    def test_post_no_ok(self, mock_get_firebase, mock_get_mongo, mock_requests):
        mockAux = MagicMock()
        mockAux.refresh.return_value = {'userId': 'userId', 'refreshToken': 'testToken'}
        mock_get_firebase.return_value = mockAux
        mockAux.auth.return_value = mockAux

        mockUsers = MagicMock()
        mockUsers.find_one.return_value = {'userId': 'userId', 'email': 'email'}

        mockDB = MagicMock()
        p1 = PropertyMock(return_value = mockUsers)
        type(mockDB).users = p1

        mockProducts = MagicMock()
        mockProducts.find_one.return_value = TestDeliveries.PRODUCT

        mockDB = MagicMock()
        p2 = PropertyMock(return_value=mockProducts)
        type(mockDB).products = p2

        mockMongo = MagicMock()
        mock_get_mongo.return_value = mockMongo
        type(mockMongo).db = PropertyMock(return_value = mockDB)

        mockPurchases = MagicMock()
        mockPurchases.find.return_value = mockPurchases
        mockPurchases.count.return_value = 5
        mockPurchases.find_one.return_value = TestDeliveries.PURCHASE

        p3 = PropertyMock(return_value = mockPurchases)
        type(mockDB).purchases = p3

        mockResponse = MagicMock()
        type(mockResponse).status_code = status.HTTP_400_BAD_REQUEST
        mockResponse.json.return_value = {'cost': '5'}
        type(mockResponse).content = {'content': 'content'}

        mock_requests.post.return_value = mockResponse

        new_delivery = {"destination_address": "Dirección Prueba",
                         "destination_latitude": "-34.592871",
                         "destination_longitude": "-58.406081"}

        response = self.app.post('/purchases/5c06f91b556f895982990e96/deliveries', json = new_delivery)
        assert status.is_server_error(response.status_code)

    @patch('src.routes.deliveries.Deliveries.get_mongo')
    @patch('src.routes.deliveries.Deliveries.get_firebase')
    def test_get_ok(self, mock_get_firebase, mock_get_mongo):
        mockAux = MagicMock()
        mockAux.refresh.return_value = {'userId': 'userId', 'refreshToken': 'testToken'}
        mock_get_firebase.return_value = mockAux
        mockAux.auth.return_value = mockAux

        mockDB = MagicMock()

        mockMongo = MagicMock()
        mock_get_mongo.return_value =  mockMongo
        type(mockMongo).db = PropertyMock(return_value = mockDB)

        mockPurchases = MagicMock()
        mockPurchases.find_one.return_value = TestDeliveries.PURCHASE

        p = PropertyMock(return_value = mockPurchases)
        type(mockDB).purchases = p

        mockDeliveries = MagicMock()
        mockDeliveries.find_one.return_value = TestDeliveries.DELIVERY

        p = PropertyMock(return_value = mockDeliveries)
        type(mockDB).deliveries = p

        response = self.app.get('/purchases/5c06f91b556f895982990e96/deliveries')
        assert status.is_success(response.status_code)