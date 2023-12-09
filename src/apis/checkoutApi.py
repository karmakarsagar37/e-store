from flask import Blueprint, request
from src.db import db

import logging

from src.services.checkout import CheckoutService
logging.basicConfig(level=logging.DEBUG)

checkout_apis = Blueprint('checkout', __name__, url_prefix="/buy")
checkoutService =  CheckoutService(database_client = db)

@checkout_apis.route('/checkout/<int:user_id>', methods = ['POST'])
def checkout(user_id):
    data = request.get_json()
    try:
        return checkoutService.checkout(user_id=user_id)
    except Exception as e:
        return {'success': False, 'error': f'Something went wrong while adding items. {str(e)}', 'message': f'{str(e)}'}, 500