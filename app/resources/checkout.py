from flask_restful import Resource, reqparse
from app.models import Cart, Product
from app.utils.db import db
import uuid

class CheckoutAPI(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('customer_id', type=int, required=True, help='Customer ID is required')
        parser.add_argument('customer_email', type=str, required=True, help='Customer email is required')
        parser.add_argument('customer_phone', type=str, required=True, help='Customer phone number is required')
        parser.add_argument('cart_id', type=int, required=True, help='Cart ID is required')
        data = parser.parse_args()

        # Check if the cart exists and is active
        cart = Cart.query.filter_by(id=data['cart_id'], user_id=data['customer_id'], status='active').first()
        if not cart:
            return {'status': 'fail', 'message': 'Active cart not found'}, 404

        # Calculate total amount
        products = Product.query.filter_by(cart_id=cart.id).all()
        if not products:
            return {'status': 'fail', 'message': 'Cart is empty'}, 400

        total_amount = sum(product.cost * product.quantity for product in products)

        # Generate a unique order ID
        order_id = str(uuid.uuid4())

        # Simulate payment process (can integrate with a payment gateway here)
        payment_details = {
            'customer_id': data['customer_id'],
            'customer_email': data['customer_email'],
            'customer_phone': data['customer_phone'],
            'order_id': order_id,
            'order_amount': total_amount,
            'order_currency': 'INR',
            'return_url': 'https://example.com/return_url'  # Replace with actual return URL
        }

        # Mark the cart as checked out
        cart.status = 'checked_out'
        cart.total_amount = total_amount
        db.session.commit()

        # Return confirmation response
        return {
            'status': 'success',
            'message': 'Checkout completed successfully',
            'order_id': order_id,
            'order_amount': total_amount,
            'payment_details': payment_details
        }, 200
