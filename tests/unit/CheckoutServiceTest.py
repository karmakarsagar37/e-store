import unittest
from unittest.mock import MagicMock, patch
from bson.objectid import ObjectId
from src.services.checkout import CheckoutService

class TestCheckoutService(unittest.TestCase):

    def setUp(self):
        self.mock_db_client = MagicMock()
        self.mock_db = self.mock_db_client.get_database.return_value
        self.mock_order_collection = MagicMock()
        self.mock_carts_collection = MagicMock()
        self.mock_items_collection = MagicMock()
        self.mock_cart_service = MagicMock()
        
        self.mock_db.get_collection.side_effect = lambda collection_name: {
            'orders': self.mock_order_collection,
            'carts': self.mock_carts_collection,
            'items': self.mock_items_collection,
        }[collection_name]
        
        self.checkout_service = CheckoutService(self.mock_db_client)
        self.checkout_service.cartService = self.mock_cart_service

    def test_checkout_with_empty_cart(self):
        user_id = 'user123'
        self.mock_carts_collection.find_one.return_value = None

        with self.assertRaises(ValueError):
            self.checkout_service.checkout(user_id)

        self.mock_carts_collection.find_one.assert_called_once_with({'user_id': user_id}, {'items': 1, 'user_id': 1})

    def test_checkout_with_discount(self):
        user_id = 'user123'
        items = [{'item_name': 'a', 'quantity': 1, 'item_price': 100}]
        total_price = 100
        self.mock_carts_collection.find_one.return_value = {'_id': ObjectId('65744ceb579c8cb22aacfde3'), 'user_id': user_id, 'items': items}
        self.mock_items_collection.find_one.return_value = {'item_price': 100}
        self.mock_order_collection.count_documents.return_value = 9  # Not a multiple of lucky_n_number
        with patch('src.services.checkout.CommonUtils.lucky_n_number', 2):  # Mocking the lucky_n_number value
            response, status_code = self.checkout_service.checkout(user_id)

        self.assertEqual(status_code, 200)
        self.assertEqual(response['message'], "Congrats you are our lucky N'th customer!. Your order will receive a special discount of 10%")
        self.assertEqual(response['grand_total'], total_price)
        self.assertEqual(response['to_pay'], 0.9 * total_price)
        self.assertEqual(response['discount'], 0.1 * total_price)
        self.mock_carts_collection.delete_one.assert_called_once()
        self.mock_order_collection.insert_one.assert_called_once()

    def test_checkout_without_discount(self):
        user_id = 'user123'
        items = [{'item_name': 'a', 'quantity': 1, 'item_price': 100}]
        total_price = 100
        self.mock_carts_collection.find_one.return_value = {'_id': ObjectId('65744ceb579c8cb22aacfde3'), 'user_id': user_id, 'items': items}
        self.mock_items_collection.find_one.return_value = {'item_price': 100}
        self.mock_order_collection.count_documents.return_value = 8  # Not a multiple of lucky_n_number
        with patch('src.services.checkout.CommonUtils.lucky_n_number', 2):  # Mocking the lucky_n_number value
            response, status_code = self.checkout_service.checkout(user_id)

        self.assertEqual(status_code, 200)
        self.assertEqual(response['message'], "Thank you for shopping with us. Visit Again!")
        self.assertEqual(response['grand_total'], total_price)
        self.assertEqual(response['to_pay'], total_price)
        self.assertEqual(response['discount'], 0)
        self.mock_carts_collection.delete_one.assert_called_once()
        self.mock_order_collection.insert_one.assert_called_once()

    @patch('src.services.checkout.logging')
    def test_abort_transaction_exception(self, mock_logging):
        user_id = 'user123'
        items = [{'item_name': 'a', 'quantity': 1, 'item_price': 100}]
        total_price = 100
        self.mock_carts_collection.find_one.return_value = {'_id': ObjectId('65744ceb579c8cb22aacfde3'), 'user_id': user_id, 'items': items}
        self.mock_items_collection.find_one.return_value = {'item_price': 100}
        self.mock_order_collection.count_documents.return_value = 8  # Not a multiple of lucky_n_number

        # Simulate an error during insert_one operation
        with patch.object(self.mock_carts_collection, 'delete_one') as mock_insert:
            mock_insert.side_effect = Exception('Simulated error')

            with self.assertRaises(ConnectionRefusedError):
                self.checkout_service.checkout(user_id)

        self.mock_order_collection.insert_one.assert_called_once()
        mock_logging.error.assert_called_once_with('Transaction aborted: Simulated error')