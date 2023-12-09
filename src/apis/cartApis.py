from flask import Blueprint, request
from src.services.cart import CartService
from src.db import db
import logging

logging.basicConfig(level=logging.INFO)

# Create a Blueprint for cart-related APIs with a specified URL prefix
cart_apis = Blueprint('cart', __name__, url_prefix="/cart")

# Initialize a CartService instance using the database client
cartService = CartService(database_client = db)

@cart_apis.route('/add/<int:user_id>', methods = ['POST'])
def add_to_cart(user_id):
    """
    Endpoint to add items to the cart for a specific user.

    Args:
        user_id (int): The ID of the user for whom items are to be added to the cart.

    Returns:
        dict: A dictionary containing either a success message or an error message in case of failure.
    """
    # Retrieve JSON data from the request
    data = request.get_json()
    try:
        # Attempt to add items to the cart using the CartService
        return cartService.add_to_cart(items=data.get('items'), user_id=user_id)
    except Exception as e:
        # Return an error response if something goes wrong during item addition
        return {'success': False, 'message': f'{str(e)}'}, 500
