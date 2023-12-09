from flask import Blueprint, request
from src.services.items import ItemService
from src.db import db
import logging

logging.basicConfig(level=logging.DEBUG)

# Create a Blueprint for item-related APIs with a specified URL prefix
items_apis = Blueprint('items', __name__, url_prefix="/items")

# Initialize an ItemService instance using the database client
itemService = ItemService(database_client=db)

@items_apis.route('/add', methods = ['POST'])
def add_items():
    """
    API endpoint used to add items to the database.

    Returns:
        dict: A dictionary containing a success message or an error message in case of failure.
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
    """
    API endpoint used to retrieve all items from the database.

    Returns:
        dict: A dictionary containing the retrieved items or an error message in case of failure.
    """
    try:
        return itemService.get_all_items()
    except Exception as e:
        return {'success': False,'message': f'{str(e)}'}, 500
