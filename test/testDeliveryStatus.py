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

class TestDeliveryStatus(TestCase):

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
                    "delivery_id": "5c06f91b556f895982990e97",
                    "user_id": "5c06f91b556f895982990e97"
                }

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.app.environ_base['HTTP_AUTHORIZATION'] = ' testToken'

    def tearDown(self):
        pass

    @patch('src.routes.deliveries.push')
    @patch('src.routes.deliveries.DeliveryStatus.get_mongo')
    @patch('src.routes.deliveries.DeliveryStatus.get_firebase')
    def test_put_ok(self, mock_get_firebase, mock_get_mongo, mock_push):
        mockAux = MagicMock()
        mockAux.refresh.return_value = {'userId': 'userId', 'refreshToken': 'testToken'}
        mock_get_firebase.return_value = mockAux
        mockAux.auth.return_value = mockAux

        mockDeliveries = MagicMock()
        mockDeliveries.find_one.return_value = TestDeliveryStatus.DELIVERY

        mockDB = MagicMock()
        p = PropertyMock(return_value = mockDeliveries)
        type(mockDB).deliveries = p

        mockMongo = MagicMock()
        mock_get_mongo.return_value =  mockMongo
        type(mockMongo).db = PropertyMock(return_value = mockDB)

        mockPurchases = MagicMock()
        mockPurchases.find_one.return_value = TestDeliveryStatus.PURCHASE

        p2 = PropertyMock(return_value=mockPurchases)
        type(mockDB).purchases = p2

        mockUsers = MagicMock()
        mockUsers.find_one.return_value = {'registration_id': 'registration_id'}

        p4 = PropertyMock(return_value=mockUsers)
        type(mockDB).users = p4

        mock_push = MagicMock()

        new_delivery_status = {"status": "Entrega Realizada"}

        response = self.app.put('/deliveries/5c06f91b556f895982990e96', json = new_delivery_status)
        assert status.is_success(response.status_code)
