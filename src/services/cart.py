from bson import ObjectId
import pymongo
import json
from bson.json_util import loads

import logging
logging.basicConfig(level=logging.INFO)

class CartService:
    def __init__(self, database_client) -> None:
        self.database_client = database_client
        self.carts_collection = self.database_client['carts']
        self.items_collection = self.database_client['items']
        
    def add_to_cart(self, items: list, user_id: str):
        cartDetails = self.carts_collection.find_one({'user_id': user_id},{'items': 1, 'user_id': 1})
        if cartDetails is None:
            currentTotal = self._calculate_total_for_items(items=items)
            self.carts_collection.insert_one({
                'user_id': user_id,
                'items': items,
                'currentTotalPrice': currentTotal
            })
            return {'success': True}, 200
        logging.info(cartDetails)
        existing_item_in_cart = cartDetails.get('items')
        current_items = self._add_new_items_to_cart(existing_items=existing_item_in_cart, new_items=items)
        currentTotal = self._calculate_total_for_items(items=current_items)
        
        filter_query = {'user_id': user_id}
        update_query = {
                'user_id': user_id,
                'items': current_items,
                'currentTotalPrice': currentTotal
            }
        self.carts_collection.update_one(filter_query, {'$set': update_query})
        return {'success': True}, 200
    def _calculate_total_for_items(self, items: list) -> int:
        logging.info("CALLED")
        total = 0
        logging.info(items)
        for item in items:
            item_id = item.get('item_name')
            item_price = self.items_collection.find_one({'_id': item_id},{'item_price': 1, '_id': 0})['item_price']
            logging.info(f'Price: {item_price}')
            total = total + (item_price * item['quantity'])
        return total
    def _add_new_items_to_cart(self, existing_items: list, new_items: list):
        for new_item in new_items:
            item_name = new_item['item_name']
            quantity = new_item['quantity']

            found = False
            for existing_item in existing_items:
                if existing_item['item_name'] == item_name:
                    existing_item['quantity'] += quantity
                    found = True
                    break

            if not found:
                existing_items.append({'item_name': item_name, 'quantity': quantity})
        return existing_items