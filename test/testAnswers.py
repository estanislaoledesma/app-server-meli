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

class TestAnswers(TestCase):

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

    ANSWERS = [
                    {
                        "_id": "5c06fc31556f895983543fb7",
                        "answer": "It's 10 pounds",
                        "user_id": "wqSsKGSFXIZoZAi931chAwbLNtF3"
                    },
                    {
                        "_id": "5c06fca0556f895983543fb8",
                        "answer": "It's 10 pounds",
                        "user_id": "wqSsKGSFXIZoZAi931chAwbLNtF3"
                    }
                ]

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.app.environ_base['HTTP_AUTHORIZATION'] = ' testToken'

    def tearDown(self):
        pass

    @patch('src.routes.answers.Answers.get_mongo')
    @patch('src.routes.answers.Answers.get_firebase')
    def test_get_ok(self, mock_get_firebase, mock_get_mongo):
        mockAux = MagicMock()
        mockAux.refresh.return_value = {'userId': 'userId', 'refreshToken': 'testToken'}
        mock_get_firebase.return_value = mockAux
        mockAux.auth.return_value = mockAux

        mockAnswers = MagicMock()
        mockAnswers.find.return_value = TestAnswers.ANSWERS

        mockDB = MagicMock()
        p = PropertyMock(return_value = mockAnswers)
        type(mockDB).answers = p

        mockMongo = MagicMock()
        mock_get_mongo.return_value =  mockMongo
        type(mockMongo).db = PropertyMock(return_value = mockDB)

        response = self.app.get('/questions/5c06f868556f89598152f2eb/answers')
        assert status.is_success(response.status_code)

    @patch('src.routes.answers.Answers.get_mongo')
    @patch('src.routes.answers.Answers.get_firebase')
    def test_post_ok(self, mock_get_firebase, mock_get_mongo):
        mockAux = MagicMock()
        mockAux.refresh.return_value = {'userId': 'userId', 'refreshToken': 'testToken'}
        mock_get_firebase.return_value = mockAux
        mockAux.auth.return_value = mockAux

        mockQuestions = MagicMock()
        mockQuestions.find_one.return_value = mockQuestions

        mockDB = MagicMock()
        p = PropertyMock(return_value = mockQuestions)
        type(mockDB).questions = p

        mockAnswers = MagicMock()
        mockAnswers.insert_one.return_value = mockAnswers
        type(mockAnswers).inserted_id = PropertyMock(return_value = 'inserted_id')

        mockDB = MagicMock()
        p1 = PropertyMock(return_value = mockAnswers)
        type(mockDB).answers = p1

        mockMongo = MagicMock()
        mock_get_mongo.return_value =  mockMongo
        type(mockMongo).db = PropertyMock(return_value = mockDB)

        new_answer = {"answer": "It's 10 pounds"}

        response = self.app.post('/questions/5c06f868556f89598152f2eb/answers', json = new_answer)
        assert status.is_success(response.status_code)

