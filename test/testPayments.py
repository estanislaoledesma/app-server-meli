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

class TestPayments(TestCase):

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
                    "payment_id": "5c06f91b556f895982990e97"
                }

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.app.environ_base['HTTP_AUTHORIZATION'] = ' testToken'

    def tearDown(self):
        pass

    @patch('src.routes.payments.requests')
    @patch('src.routes.payments.Payments.get_mongo')
    @patch('src.routes.payments.Payments.get_firebase')
    def test_post_ok(self, mock_get_firebase, mock_get_mongo, mock_requests):
        mockAux = MagicMock()
        mockAux.refresh.return_value = {'userId': 'userId', 'refreshToken': 'testToken'}
        mock_get_firebase.return_value = mockAux
        mockAux.auth.return_value = mockAux

        mockPurchase = MagicMock()
        mockPurchase.find_one.return_value = TestPayments.PURCHASE

        mockDB = MagicMock()
        p = PropertyMock(return_value = mockPurchase)
        type(mockDB).purchases = p

        mockMongo = MagicMock()
        mock_get_mongo.return_value =  mockMongo
        type(mockMongo).db = PropertyMock(return_value = mockDB)

        mockPayment = MagicMock()
        type(mockPayment).inserted_id = PropertyMock(return_value = "inserted_id")

        mockPayments = MagicMock()
        mockPayments.insert_one.return_value = mockPayment

        p2 = PropertyMock(return_value = mockPayments)
        type(mockDB).payments = p2

        new_payment = {"payment_method": "credit",
                        "card_number": "4237349324",
                        "card_cvc": "998",
                        "card_expiration_year": "2021",
                        "card_expiration_month": "04",
                        "card_holder": "Estanislao Ledesma"}

        mockResponse = MagicMock()
        type(mockResponse).status_code = status.HTTP_201_CREATED

        mock_requests.post.return_value = mockResponse

        mockPurchases = MagicMock()

        p3 = PropertyMock(return_value=mockPurchases)
        type(mockDB).purchases = p2

        response = self.app.post('/purchases/5c06f91b556f895982990e96/payments', json = new_payment)
        assert status.is_success(response.status_code)

    @patch('src.routes.payments.requests')
    @patch('src.routes.payments.Payments.get_mongo')
    @patch('src.routes.payments.Payments.get_firebase')
    def test_post_no_ok(self, mock_get_firebase, mock_get_mongo, mock_requests):
        mockAux = MagicMock()
        mockAux.refresh.return_value = {'userId': 'userId', 'refreshToken': 'testToken'}
        mock_get_firebase.return_value = mockAux
        mockAux.auth.return_value = mockAux

        mockPurchase = MagicMock()
        mockPurchase.find_one.return_value = TestPayments.PURCHASE

        mockDB = MagicMock()
        p = PropertyMock(return_value=mockPurchase)
        type(mockDB).purchases = p

        mockMongo = MagicMock()
        mock_get_mongo.return_value = mockMongo
        type(mockMongo).db = PropertyMock(return_value=mockDB)

        mockPayment = MagicMock()
        type(mockPayment).inserted_id = PropertyMock(return_value="inserted_id")

        mockPayments = MagicMock()
        mockPayments.insert_one.return_value = mockPayment

        p2 = PropertyMock(return_value=mockPayments)
        type(mockDB).payments = p2

        new_payment = {"payment_method": "credit",
                       "card_number": "4237349324",
                       "card_cvc": "998",
                       "card_expiration_year": "2021",
                       "card_expiration_month": "04",
                       "card_holder": "Estanislao Ledesma"}

        mockResponse = MagicMock()
        type(mockResponse).status_code = status.HTTP_400_BAD_REQUEST
        type(mockResponse).content = {'content': 'content'}

        mock_requests.post.return_value = mockResponse

        mockPurchases = MagicMock()

        p3 = PropertyMock(return_value=mockPurchases)
        type(mockDB).purchases = p2

        response = self.app.post('/purchases/5c06f91b556f895982990e96/payments', json=new_payment)
        assert status.is_server_error(response.status_code)


    @patch('src.routes.payments.requests')
    @patch('src.routes.payments.Payments.get_mongo')
    @patch('src.routes.payments.Payments.get_firebase')
    def test_get_ok(self, mock_get_firebase, mock_get_mongo, mock_requests):
        mockAux = MagicMock()
        mockAux.refresh.return_value = {'userId': 'userId', 'refreshToken': 'testToken'}
        mock_get_firebase.return_value = mockAux
        mockAux.auth.return_value = mockAux

        mockPurchase = MagicMock()
        mockPurchase.find_one.return_value = TestPayments.PURCHASE

        mockDB = MagicMock()
        p = PropertyMock(return_value=mockPurchase)
        type(mockDB).purchases = p

        mockMongo = MagicMock()
        mock_get_mongo.return_value = mockMongo
        type(mockMongo).db = PropertyMock(return_value=mockDB)

        mockPayments = MagicMock()
        mockPayments.find_one.return_value = TestPayments.PAYMENT

        p2 = PropertyMock(return_value=mockPayments)
        type(mockDB).payments = p2

        response = self.app.get('/purchases/5c06f91b556f895982990e96/payments')
        assert status.is_success(response.status_code)
