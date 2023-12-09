import unittest
from unittest.mock import MagicMock
from src.db import db_name
from src.services.cart import CartService

class TestCartService(unittest.TestCase):

    def setUp(self):
        self.mock_database_client = MagicMock()
        self.mock_database = MagicMock()
        self.mock_carts_collection = MagicMock()
        self.mock_items_collection = MagicMock()
        
        self.mock_database_client.get_database.return_value = self.mock_database
        self.mock_database.get_collection.side_effect = lambda collection: {
            'carts': self.mock_carts_collection,
            'items': self.mock_items_collection
        }[collection]

        self.cart_service = CartService(self.mock_database_client)

    def test_add_to_cart_new_user(self):
        # Set up mocks
        self.mock_carts_collection.find_one.return_value = None
        self.mock_items_collection.find_one.return_value = {'item_price': 10}

        # Test adding items for a new user
        items = [{'item_name': 'item1', 'quantity': 2}, {'item_name': 'item2', 'quantity': 3}]
        user_id = 'user123'

        result, status_code = self.cart_service.add_to_cart(items, user_id)

        # Assertions
        self.assertTrue(result['success'])
        self.assertEqual(status_code, 200)
        self.mock_carts_collection.insert_one.assert_called_once()

    def test_add_to_cart_existing_user(self):
        # Set up mocks
        existing_cart = {
            'user_id': 'user123',
            'items': [{'item_name': 'item1', 'quantity': 2}],
            'currentTotalPrice': 20
        }
        self.mock_carts_collection.find_one.return_value = existing_cart
        self.mock_items_collection.find_one.return_value = {'item_price': 10}

        # Test adding items for an existing user
        items = [{'item_name': 'item2', 'quantity': 3}]
        user_id = 'user123'

        result, status_code = self.cart_service.add_to_cart(items, user_id)

        # Assertions
        self.assertTrue(result['success'])
        self.assertEqual(status_code, 200)
        self.mock_carts_collection.update_one.assert_called_once()

if __name__ == '__main__':
    unittest.main()
