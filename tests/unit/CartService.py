import unittest
from unittest.mock import MagicMock, patch
from bson import ObjectId
from pymongo.collection import Collection
from src.services.cart import CartService

# from  import CartService

# Import your CartService class here...

class CartServicetest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mock_client = MagicMock()
        cls.mock_db = MagicMock()
        cls.mock_items_collection = MagicMock(spec=Collection)
        cls.mock_carts_collection = MagicMock(spec=Collection)

        cls.mock_client.__getitem__.side_effect = [cls.mock_db, cls.mock_carts_collection, cls.mock_items_collection]

        cls.cart_service = CartService(cls.mock_client)

    def test_add_to_cart_new_user(self):
        # Mocking data
        user_id = 'user123'
        items = [{'item_name': 'item1', 'quantity': 2}, {'item_name': 'item2', 'quantity': 3}]

        # Mocking the return value for find_one when user is not found
        self.mock_carts_collection.find_one.return_value = None

        # Mocking the item price retrieval
        self.mock_items_collection.find_one.return_value = {'item_price': 10}

        # Test add_to_cart for a new user
        response, status_code = self.cart_service.add_to_cart(items, user_id)

        # Assertions
        self.assertEqual(status_code, 200)
        self.assertTrue(response['success'])
        self.mock_carts_collection.insert_one.assert_called_once()

    def test_add_to_cart_existing_user(self):
        # Mocking data
        user_id = 'user123'
        existing_items = [{'item_name': 'item1', 'quantity': 1}, {'item_name': 'item2', 'quantity': 2}]
        new_items = [{'item_name': 'item1', 'quantity': 2}, {'item_name': 'item3', 'quantity': 1}]

        # Mocking the return value for find_one when user is found
        self.mock_carts_collection.find_one.return_value = {'user_id': user_id, 'items': existing_items}

        # Mocking the item price retrieval
        self.mock_items_collection.find_one.return_value = {'item_price': 20}

        # Test add_to_cart for an existing user
        response, status_code = self.cart_service.add_to_cart(new_items, user_id)

        # Assertions
        self.assertEqual(status_code, 200)
        self.assertTrue(response['success'])
        self.mock_carts_collection.update_one.assert_called_once()

if __name__ == '__main__':
    unittest.main()
