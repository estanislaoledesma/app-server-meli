import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
        resultado = self.app.get('/)
        assert resultado.get_json(force=True) ['Hello'] == 'World'

    def test_sign_up(self):
        email = 'test@domain.com'
        password = 'password'
        resultado = self.app.post('/signup', data = dict(email = email, password = password), follow_redirects = True)
        assert resultado.get_json(force=True) ['code'] == Config.CODE_OK