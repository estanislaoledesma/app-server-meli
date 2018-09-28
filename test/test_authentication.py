import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_api import status

from unittest import TestCase

from src.settings.application import app
from src.settings.application import Config

class Test_Authetication(TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_hello_world(self):
        response = self.app.get('/')
        assert response.get_json(force=True) ['Hello'] == 'World'

    def test_sign_up(self):
        display_name = 'Test'
        email = 'test@domain.com'
        password = 'password'
        response = self.app.post('/signup', json = {'display_name': display_name, 'email': email, 'password': password})
        assert status.is_success(response.status_code)