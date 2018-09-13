from flask import Flask
from flask_restful import Resource, Api
from flask_marshmallow import Marshmallow
from src.routes import hello, user

app = Flask(__name__)
api = Api(app)
ma = Marshmallow(app)

api.add_resource(hello.HelloWorld, '/')
api.add_resource(user.Sign_Up, '/signup')