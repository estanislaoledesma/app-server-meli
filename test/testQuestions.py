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

class TestQuestions(TestCase):

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

    QUESTIONS = [
                    {
                        "_id": "5c06fbc9556f8959845d3767",
                        "question": "Cuánto sale?"
                    }
                ]

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.app.environ_base['HTTP_AUTHORIZATION'] = ' testToken'

    def tearDown(self):
        pass

    @patch('src.routes.questions.Questions.get_mongo')
    @patch('src.routes.questions.Questions.get_firebase')
    def test_get_ok(self, mock_get_firebase, mock_get_mongo):
        mockAux = MagicMock()
        mockAux.refresh.return_value = {'userId': 'userId', 'refreshToken': 'testToken'}
        mock_get_firebase.return_value = mockAux
        mockAux.auth.return_value = mockAux

        mockQuestions = MagicMock()
        mockQuestions.find.return_value = TestQuestions.QUESTIONS

        mockDB = MagicMock()
        p = PropertyMock(return_value = mockQuestions)
        type(mockDB).questions = p

        mockMongo = MagicMock()
        mock_get_mongo.return_value =  mockMongo
        type(mockMongo).db = PropertyMock(return_value = mockDB)

        response = self.app.get('/products/5c06f868556f89598152f2eb/questions')
        assert status.is_success(response.status_code)

    @patch('src.routes.questions.Questions.get_mongo')
    @patch('src.routes.questions.Questions.get_firebase')
    def test_post_ok(self, mock_get_firebase, mock_get_mongo):
        mockAux = MagicMock()
        mockAux.refresh.return_value = {'userId': 'userId', 'refreshToken': 'testToken'}
        mock_get_firebase.return_value = mockAux
        mockAux.auth.return_value = mockAux

        mockQuestions = MagicMock()
        mockQuestions.insert_one.return_value = mockQuestions
        type(mockQuestions).inserted_id = PropertyMock(return_value = 'inserted_id')

        mockDB = MagicMock()
        p = PropertyMock(return_value = mockQuestions)
        type(mockDB).questions = p

        mockProducts = MagicMock()
        mockProducts.find_one.return_value = TestQuestions.PRODUCT

        p = PropertyMock(return_value = mockProducts)
        type(mockDB).products = p

        mockMongo = MagicMock()
        mock_get_mongo.return_value =  mockMongo
        type(mockMongo).db = PropertyMock(return_value = mockDB)

        new_question = {"question": "Cuánto sale?"}

        response = self.app.post('/products/5c06f868556f89598152f2eb/questions', json = new_question)
        assert status.is_success(response.status_code)

