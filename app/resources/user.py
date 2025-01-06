from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app.utils.db import db

class UserRegisterAPI(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name is required')
        parser.add_argument('email', type=str, required=True, help='Email is required')
        parser.add_argument('password', type=str, required=True, help='Password is required')
        data = parser.parse_args()

        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return {'status': 'fail', 'message': 'Email already registered'}, 400

        # Hash the password
        hashed_password = generate_password_hash(data['password'], method='sha256')

        # Create a new user
        new_user = User(name=data['name'], email=data['email'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return {'status': 'success', 'message': 'User registered successfully'}, 201


class UserLoginAPI(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help='Email is required')
        parser.add_argument('password', type=str, required=True, help='Password is required')
        data = parser.parse_args()

        # Check if user exists
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            return {'status': 'fail', 'message': 'User not found'}, 404

        # Verify password
        if not check_password_hash(user.password, data['password']):
            return {'status': 'fail', 'message': 'Invalid credentials'}, 401

            # Return user info (Here you can implement session/token-based authentication later)
        return {
            'status': 'success',
            'message': 'Login successful',
            'user_id': user.id,
            'user_name': user.name
        }, 200
