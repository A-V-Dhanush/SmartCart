from flask_restful import Resource, reqparse
from app.models import Cart, Product
from app.utils.db import db

class AddProductAPI(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cart_id', type=int, required=True, help='Cart ID is required')
        parser.add_argument('product_id', type=int, required=True, help='Product ID is required')
        parser.add_argument('product_name', type=str, required=True, help='Product name is required')
        parser.add_argument('cost', type=float, required=True, help='Product cost is required')
        parser.add_argument('quantity', type=int, required=True, help='Quantity is required')
        data = parser.parse_args()

        # Check if the cart exists and is active
        cart = Cart.query.filter_by(id=data['cart_id'], status='active').first()
        if not cart:
            return {'status': 'fail', 'message': 'Active cart not found'}, 404

        # Add or update product in the cart
        product = Product.query.filter_by(cart_id=cart.id, id=data['product_id']).first()
        if product:
            product.quantity += data['quantity']  # Update quantity if product already exists
        else:
            product = Product(
                id=data['product_id'],
                product_name=data['product_name'],
                cost=data['cost'],
                quantity=data['quantity'],
                cart_id=cart.id
            )
            db.session.add(product)

        db.session.commit()
        return {'status': 'success', 'message': 'Product added/updated successfully'}, 200


class RemoveProductAPI(Resource):
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cart_id', type=int, required=True, help='Cart ID is required')
        parser.add_argument('product_id', type=int, required=True, help='Product ID is required')
        data = parser.parse_args()

        # Check if the cart exists and is active
        cart = Cart.query.filter_by(id=data['cart_id'], status='active').first()
        if not cart:
            return {'status': 'fail', 'message': 'Active cart not found'}, 404

        # Remove product from the cart
        product = Product.query.filter_by(cart_id=cart.id, id=data['product_id']).first()
        if not product:
            return {'status': 'fail', 'message': 'Product not found in cart'}, 404

        db.session.delete(product)
        db.session.commit()

        return {'status': 'success', 'message': 'Product removed successfully'}, 200
