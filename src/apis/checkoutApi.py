from flask import Blueprint, request
from src.db import db
import logging
from src.services.checkout import CheckoutService

logging.basicConfig(level=logging.INFO)

# Create a Blueprint for checkout-related APIs with a specified URL prefix
checkout_apis = Blueprint('checkout', __name__, url_prefix="/buy")

# Initialize a CheckoutService instance using the database client
checkoutService = CheckoutService(database_client = db)

@checkout_apis.route('/checkout/<int:user_id>', methods = ['POST'])
def checkout(user_id):
    """
    API endpoint used to perform the checkout process for a specific user.

    Args:
        user_id (int): The ID of the user for whom the checkout process is performed.

    Returns:
        dict: A dictionary containing a success message or an error message in case of failure.
    """
    try:
        # Attempt to perform the checkout process using the CheckoutService
        return checkoutService.checkout(user_id=user_id)
    except Exception as e:
        # Return an error response if something goes wrong during checkout
        return {
            'success': False,
            'message': f'{str(e)}'
        }, 500
