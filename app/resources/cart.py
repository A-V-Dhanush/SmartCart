from flask_restful import Resource, reqparse
from app.models import Cart, Product, User
from app.utils.db import db

class ScanCartAPI(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cart_id', type=int, required=True, help='Cart ID is required')
        parser.add_argument('user_id', type=int, required=True, help='User ID is required')
        data = parser.parse_args()

        # Check if user exists
        user = User.query.get(data['user_id'])
        if not user:
            return {'status': 'fail', 'message': 'User not found'}, 404

        # Check if cart exists or create a new one
        cart = Cart.query.filter_by(id=data['cart_id'], user_id=data['user_id'], status='active').first()
        if not cart:
            cart = Cart(id=data['cart_id'], user_id=data['user_id'])
            db.session.add(cart)
            db.session.commit()

        return {'status': 'success', 'message': 'Cart linked successfully', 'cart_id': cart.id}, 200


class CartAPI(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cart_id', type=int, required=True, help='Cart ID is required')
        parser.add_argument('user_id', type=int, required=True, help='User ID is required')
        data = parser.parse_args()

        # Fetch cart and its products
        cart = Cart.query.filter_by(id=data['cart_id'], user_id=data['user_id'], status='active').first()
        if not cart:
            return {'status': 'fail', 'message': 'Active cart not found'}, 404

        products = Product.query.filter_by(cart_id=cart.id).all()
        products_data = [
            {
                'product_id': product.id,
                'product_name': product.product_name,
                'cost': product.cost,
                'quantity': product.quantity
            }
            for product in products
        ]

        return {'status': 'success', 'cart_id': cart.id, 'products': products_data}, 200
