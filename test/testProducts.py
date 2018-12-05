import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_api import status

from unittest import TestCase
from mock import patch, MagicMock, PropertyMock

sys.modules['pyrebase'] = MagicMock()
from src.settings.application import app

class TestProducts(TestCase):

    PRODUCTS = [
                    {
                        "_id": "id1",
                        "name": "Producto Test1",
                        "price": 50,
                        "images": []
                    },
                    {
                        "_id": "id2",
                        "name": "Producto Test2",
                        "price": 59,
                        "images": []
                    }
                ]
    PRODUCT = {"product":
                            {"name": "Producto Test",
                            "description": "Producto de prueba",
                            "images": "",
                            "price": 50,
                            "category": "Categoría Test",
                            "ubication": "Ubicación Test",
                            "latitude": "-34.583540",
                            "longitude": "-58.406081",
                            "units": 1}
                }

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.app.environ_base['HTTP_AUTHORIZATION'] = ' testToken'

    def tearDown(self):
        pass

    @patch('src.routes.products.Products.get_mongo')
    @patch('src.routes.products.Products.get_firebase')
    def test_get_ok(self, mock_get_firebase, mock_get_mongo):
        mockAux = MagicMock()
        mockAux.refresh.return_value = {'refreshToken': 'testToken'}
        mock_get_firebase.return_value = mockAux
        mockAux.auth.return_value = mockAux

        mockProducts = MagicMock()
        mockProducts.find.return_value = TestProducts.PRODUCTS

        p = PropertyMock(return_value = mockProducts)
        type(mock_get_mongo.db).users = p

        response = self.app.get('/products')
        assert status.is_success(response.status_code)

    @patch('src.routes.products.Products.get_mongo')
    @patch('src.routes.products.Products.get_firebase')
    def test_post_ok(self, mock_get_firebase, mock_get_mongo):
        mockAux = MagicMock()
        mockAux.refresh.return_value = {'userId': 'userId', 'refreshToken': 'testToken'}
        mock_get_firebase.return_value = mockAux
        mockAux.auth.return_value = mockAux

        mockUser = MagicMock()
        id = PropertyMock(return_value = "inserted_id")
        type(mockUser).inserted_id = id

        mockUsers = MagicMock()
        mockUsers.insert_one.return_value = mockUser

        p = PropertyMock(return_value=mockUsers)
        type(mock_get_mongo.db).users = p

        response = self.app.post('/products', json = TestProducts.PRODUCT)
        assert status.is_success(response.status_code)
