from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from app.utils.db import init_db

# Initialize Flask App
app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize Extensions
db = SQLAlchemy(app)
api = Api(app)

# Import Resources and Add Routes
from app.resources.user import UserRegisterAPI, UserLoginAPI
from app.resources.cart import CartAPI, ScanCartAPI
from app.resources.checkout import CheckoutAPI

# Add API Endpoints
api.add_resource(UserRegisterAPI, '/user/register')
api.add_resource(UserLoginAPI, '/user/login')
api.add_resource(ScanCartAPI, '/cart/identify')
api.add_resource(CartAPI, '/cart/products')
api.add_resource(CheckoutAPI, '/checkout')

# Initialize Database
with app.app_context():
    init_db()
