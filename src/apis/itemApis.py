from flask import Blueprint, request, jsonify
from src.services.items import ItemService
from src.db import db

import logging
logging.basicConfig(level=logging.DEBUG)

items_apis = Blueprint('items', __name__,url_prefix="/items")
itemService =  ItemService(database_client = db)

@items_apis.route('/add', methods = ['POST'])
def add_items():
    """API used to add items in Database

    Returns:
        _type_: A
    """
    data = request.get_json()
    logging.info(data)
    items = data.get('items')
    try:
        return itemService.add_items(items)
    except Exception as e:
        return {'success': False, 'error': f'Something went wrong while adding items with Error Message: {str(e)}'}, 500
    
@items_apis.route('/get', methods = ['GET'])
def query_example():
    try:
        return itemService.get_all_items()
    except Exception as e:
        return {'success': False, 'error': f'Something went wrong while Getting items with Error Message: {str(e)}'}, 500