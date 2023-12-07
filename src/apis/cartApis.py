from flask import Blueprint, request
from src.services.cart import CartService
from src.db import db

import logging
logging.basicConfig(level=logging.DEBUG)

cart_apis = Blueprint('cart', __name__, url_prefix="/cart")
cartService =  CartService(database_client = db)

@cart_apis.route('/add/<int:user_id>', methods = ['POST'])
def add_to_cart(user_id):
    data = request.get_json()
    try:
        return cartService.add_to_cart(items=data.get('items'), user_id=user_id)
    except Exception as e:
        return {'success': False, 'error': f'Something went wrong while adding items. {str(e)}'}, 500