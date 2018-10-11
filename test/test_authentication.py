import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_api import status

from unittest import TestCase
from mock import patch, MagicMock, PropertyMock

from src.settings.application import app
from src.routes.user import SignUp, Login

class Test_Authetication(TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_hello_world(self):
        response = self.app.get('/')
        assert response.get_json(force=True) ['Hello'] == 'World'

    @patch('src.routes.user.SignUp.get_firebase')
    def test_sign_up(self, mock_get_firebase):
        display_name = 'Test'
        email = 'test@domain.com'
        password = 'password'

        mockAux = MagicMock()
        mockAux.create_user_with_email_and_password.return_value = {'refreshToken': 'testToken'}
        mock_get_firebase.auth.return_value = mockAux

        response = self.app.post('/signup', json = {'display_name': display_name, 'email': email, 'password': password})
        assert status.is_success(response.status_code)
