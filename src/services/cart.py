import logging
import pymongo
from src.db import db_name

logging.basicConfig(level=logging.INFO)

class CartService:
    def __init__(self, database_client: pymongo.MongoClient) -> None:
        """
        Initializes CartService with the required database collections.

        Args:
            database_client (pymongo.MongoClient): The MongoDB client.
        """
        self.database_client = database_client
        self.database = database_client.get_database(db_name)
        self.carts_collection = self.database.get_collection('carts')
        self.items_collection = self.database.get_collection('items')

    def add_to_cart(self, items: list, user_id: str):
        """
        Adds items to a user's cart or updates existing items in the cart.

        Args:
            items (list): List of items to add or update in the cart.
            user_id (str): ID of the user whose cart is being updated.

        Returns:
            dict: Success message with cart details or error message.
        """
        cart_details = self.carts_collection.find_one({'user_id': user_id}, {'items': 1, 'user_id': 1})

        if cart_details is None:
            items = self._update_price_of_items(items=items)
            current_total = self._calculate_total_for_items(items=items)
            cart_data = {
                'user_id': user_id,
                'items': items,
                'currentTotalPrice': current_total
            }
            self.carts_collection.insert_one(cart_data)
            return {'success': True, 'cart': {
                'user_id': user_id,
                'items': items,
                'currentTotalPrice': current_total
            }}, 200

        existing_items = cart_details.get('items')
        current_items = self._add_new_items_to_cart(existing_items=existing_items, new_items=items)
        current_items = self._update_price_of_items(items=current_items)
        current_total = self._calculate_total_for_items(items=current_items)

        filter_query = {'user_id': user_id}
        update_query = {
            'user_id': user_id,
            'items': current_items,
            'currentTotalPrice': current_total
        }
        self.carts_collection.update_one(filter_query, {'$set': update_query})
        return {'success': True, 'cart': update_query}, 200

    def _calculate_total_for_items(self, items: list) -> int:
        """
        Calculates the total price for a list of items.

        Args:
            items (list): List of items with quantities.

        Returns:
            int: Total price for the items.
        """
        return sum(item['item_price'] * item['quantity'] for item in items)

    def _add_new_items_to_cart(self, existing_items: list, new_items: list):
        """
        Adds new items to the existing cart items or updates quantities if items already exist.

        Args:
            existing_items (list): List of items already present in the cart.
            new_items (list): List of new items to be added to the cart.

        Returns:
            list: Updated list of cart items.
        """
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

    def _update_price_of_items(self, items: list) -> list:
        """
        Adds prices to the items.

        Args:
            items (list): List of items to add prices to.

        Returns:
            list: List of items with prices added.
        """
        for item in items:
            item_id = item.get('item_name')
            itemDetail = self.items_collection.find_one({'_id': item_id}, {'item_price': 1, '_id': 0})
            item['item_price'] = itemDetail['item_price']
        return items
