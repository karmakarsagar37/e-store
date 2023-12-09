import unittest
from pymongo.errors import PyMongoError
from unittest.mock import MagicMock, patch
from pymongo import MongoClient
from src.services.cart import CartService
from src.utils.common_utils import CommonUtils
from src.services.checkout import CheckoutService

class TestCheckoutService(unittest.TestCase):

    def setUp(self):
        self.mock_db_client = MagicMock(spec=MongoClient)
        self.mock_cart_service = MagicMock(spec=CartService)
        self.checkout_service = CheckoutService(self.mock_db_client)
        self.checkout_service.cartService = self.mock_cart_service

    def test_checkout_empty_cart(self):
        # Simulate an empty cart for a user
        user_id = 'user123'
        self.checkout_service.carts_collection.find_one.return_value = None

        with self.assertRaises(ValueError) as context:
            self.checkout_service.checkout(user_id)

        self.assertEqual(str(context.exception), "User cart is empty! Please add items to checkout")

    @patch('src.services.checkout.logging')
    @patch('src.services.checkout.CommonUtils')
    def test_checkout_lucky_customer_discount(self, mock_common_utils, mock_logging):
        user_id = 'user456'
        items_in_cart = [{'item_id': 1, 'name': 'Product A', 'price': 20}, {'item_id': 2, 'name': 'Product B', 'price': 30}]
        total_price = sum(item['price'] for item in items_in_cart)

        self.checkout_service.carts_collection.find_one.return_value = {'user_id': user_id, 'items': items_in_cart}
        self.checkout_service.order_collection.count_documents.return_value = 9  # Assuming 9 orders till now
        self.mock_cart_service._calculate_total_for_items.return_value = total_price
        mock_common_utils.lucky_n_number = 10
        
        response, status_code = self.checkout_service.checkout(user_id)

        self.assertEqual(status_code, 200)
        self.assertEqual(response['message'], "Congrats you are our lucky N'th customer!. Your order will receive a special discount of 10%")
        self.assertEqual(response['items'], items_in_cart)
        self.assertEqual(response['grand_total'], total_price)
        self.assertEqual(response['disount'], 0.10 * total_price)
        self.assertEqual(response['to_pay'], 0.90 * total_price)

    @patch('src.services.checkout.logging')
    @patch('src.services.checkout.CommonUtils')
    def test_checkout_regular_customer(self, mock_common_utils, mock_logging):
        user_id = 'user789'
        items_in_cart = [{'item_id': 3, 'name': 'Product C', 'price': 25}, {'item_id': 4, 'name': 'Product D', 'price': 35}]
        total_price = sum(item['price'] for item in items_in_cart)

        self.checkout_service.carts_collection.find_one.return_value = {'user_id': user_id, 'items': items_in_cart}
        self.checkout_service.order_collection.count_documents.return_value = 5  # Assuming 5 orders till now
        mock_common_utils.lucky_n_number = 10  # Setting a different lucky number for testing
        self.mock_cart_service._calculate_total_for_items.return_value = total_price

        response, status_code = self.checkout_service.checkout(user_id)

        self.assertEqual(status_code, 200)
        self.assertEqual(response['message'], "Thank you for shopping with us. Visit Again!")
        self.assertEqual(response['items'], items_in_cart)
        self.assertEqual(response['grand_total'], total_price)
        self.assertEqual(response['disount'], 0)
        self.assertEqual(response['to_pay'], total_price)
    
    
    @patch('src.services.checkout.logging')
    def test_checkout_mongo_transaction_failure(self, mock_logging):
        user_id = 'user999'
        items_in_cart = [{'item_id': 5, 'name': 'Product E', 'price': 40}, {'item_id': 6, 'name': 'Product F', 'price': 50}]
        total_price = sum(item['price'] for item in items_in_cart)

        self.checkout_service.carts_collection.find_one.return_value = {'user_id': user_id, 'items': items_in_cart}
        self.checkout_service.order_collection.count_documents.return_value = 7  # Assuming 7 orders till now
        self.mock_cart_service._calculate_total_for_items.return_value = total_price

        # Simulate a MongoDB transaction failure during order insertion
        mock_session = self.mock_db_client.start_session()
        mock_session.__enter__.return_value = mock_session
        mock_session.__exit__.return_value = None
        mock_session.start_transaction.return_value = None
        mock_session.commit_transaction.side_effect = PyMongoError

        with patch.object(self.mock_db_client, 'start_session', return_value=mock_session):
            with self.assertRaises(ConnectionRefusedError) as context:
                self.checkout_service.checkout(user_id)

        self.assertEqual(str(context.exception), 'Error while writing in db!')
        mock_session.abort_transaction.assert_called_once()


if __name__ == '__main__':
    unittest.main()
