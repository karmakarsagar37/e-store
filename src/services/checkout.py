import logging
import pymongo
from src.utils.common_utils import CommonUtils
logging.basicConfig(level=logging.INFO)  # Configuring the logging level to INFO
from src.db import db_name  # Importing the database name from configuration

class CheckoutService:
    def __init__(self, database_client: pymongo.MongoClient) -> None:
        # Initializing CheckoutService with a MongoDB database client
        self.database_client = database_client
        self.database = database_client.get_database(db_name)  # Getting the specified database
        # Getting collections from the database
        self.order_collection = self.database.get_collection('orders')
        self.carts_collection = self.database.get_collection('carts')
        self.items_collection = self.database.get_collection('items')
        
    def checkout(self, user_id: str):
        # Retrieving cart details for the given user
        cartDetails = self.carts_collection.find_one({'user_id': user_id},{'items': 1, 'user_id': 1})
        if cartDetails is None:
            # Raise an error if the user's cart is empty
            raise ValueError("User cart is empty! Please add items to checkout")
        
        existing_items = cartDetails.get('items')
        # Updating prices of items in the cart
        existing_items = self._update_price_of_items(items=existing_items)
        # Calculating the total price of items in the cart
        total = sum(item['item_price'] * item['quantity'] for item in existing_items)
        logging.info(total)  # Logging the total price
        
        orders_till_now = self.order_collection.count_documents({})
        response = {}
        # Checking if the user's order makes them eligible for a special discount
        if (orders_till_now + 1) % CommonUtils.lucky_n_number == 0:
            response = {
                "message": "Congrats you are our lucky N'th customer!. Your order will receive a special discount of 10%",
                "items": existing_items,
                "grand_total": total,
                "discount": (0.10 * total),
                "to_pay": (0.90 * total)
            }
        else:
            response = {
                "message": "Thank you for shopping with us. Visit Again!",
                "items": existing_items,
                "grand_total": total,
                "discount": 0,
                "to_pay": total
            }
        
        # Performing transactional operations for order placement and cart clearance
        with self.database_client.start_session() as session:
            try:
                # Perform operations within the transaction
                with session.start_transaction():
                    # Inserting order details into the 'orders' collection
                    self.order_collection.insert_one({'user_id': user_id, 'order_details': response}, session=session)
                    # Deleting the user's cart from the 'carts' collection
                    self.carts_collection.delete_one({'user_id': user_id}, session=session)
                # Committing the transaction
                session.commit_transaction()
                logging.info("Transaction committed successfully")

            except Exception as e:
                # Rollback the transaction if any error occurs
                session.abort_transaction()
                logging.error(f"Transaction aborted: {e}")
                raise ConnectionRefusedError('Error while writing in db!')
        
        return response, 200
    
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
            # Fetching the item's price from the 'items' collection in the database. This is done so that we take the latest price while calculating the grand total
            itemDetail = self.items_collection.find_one({'_id': item_id}, {'item_price': 1, '_id': 0})
            item['item_price'] = itemDetail['item_price']
        return items
