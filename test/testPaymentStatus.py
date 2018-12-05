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

class TestPaymentStatus(TestCase):

    PAYMENT = {
                    "_id": "5c06fa31556f895983543fb6",
                    "currency": "ARS",
                    "paymentMethod": {
                        "expiration_month": "04",
                        "expiration_year": "2021",
                        "method": "credit",
                        "number": "4237349324",
                        "type": "credit"
                    },
                    "status": "Pago Aceptado",
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

    @patch('src.routes.payments.push')
    @patch('src.routes.payments.PaymentStatus.get_mongo')
    @patch('src.routes.payments.PaymentStatus.get_firebase')
    def test_put_ok(self, mock_get_firebase, mock_get_mongo, mock_push):
        mockAux = MagicMock()
        mockAux.refresh.return_value = {'userId': 'userId', 'refreshToken': 'testToken'}
        mock_get_firebase.return_value = mockAux
        mockAux.auth.return_value = mockAux

        mockPayments = MagicMock()

        mockDB = MagicMock()
        p = PropertyMock(return_value = mockPayments)
        type(mockDB).payments = p

        mockMongo = MagicMock()
        mock_get_mongo.return_value =  mockMongo
        type(mockMongo).db = PropertyMock(return_value = mockDB)

        mockPurchases = MagicMock()
        mockPurchases.find_one.return_value = TestPaymentStatus.PURCHASE

        p2 = PropertyMock(return_value=mockPurchases)
        type(mockDB).purchases = p2

        mockDeliveries = MagicMock()

        p3 = PropertyMock(return_value=mockDeliveries)
        type(mockDB).deliveries = p3

        mockUsers = MagicMock()
        mockUsers.find_one.return_value = {'registration_id': 'registration_id'}

        p4 = PropertyMock(return_value=mockUsers)
        type(mockDB).users = p4

        mock_push = MagicMock()

        new_payment_status = {"status": "Pago Aceptado",
                             "tracking_id": "1000"}

        response = self.app.put('/payments/5c06f91b556f895982990e96', json = new_payment_status)
        assert status.is_success(response.status_code)
