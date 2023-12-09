import logging
import pymongo
from src.services.cart import CartService
from src.utils.common_utils import CommonUtils
logging.basicConfig(level=logging.INFO)
from src.db import db_name

class CheckoutService:
    def __init__(self, database_client: pymongo.MongoClient) -> None:
        self.database_client = database_client
        self.database = database_client.get_database(db_name)
        self.order_collection = self.database.get_collection('orders')
        self.carts_collection = self.database.get_collection('carts')
        self.cartService = CartService(database_client=database_client)

    def checkout(self, user_id: str):
        cartDetails = self.carts_collection.find_one({'user_id': user_id},{'items': 1, 'user_id': 1})
        if cartDetails is None:
            raise ValueError("User cart is empty! Please add items to checkout")
        existing_items = cartDetails.get('items')
        total = self.cartService._calculate_total_for_items(items=existing_items)
        logging.info(total)
        orders_till_now = self.order_collection.count_documents({})
        response = {}
        if (orders_till_now + 1) % CommonUtils.lucky_n_number == 0:
            response = {
                "message": "Congrats you are our lucky N'th customer!. Your order will receive a special discount of 10%",
                "items": existing_items,
                "grand_total": total,
                "disount": (0.10* total),
                "to_pay": (0.90 * total)
            }
        else:
            response = {
                "message": "Thank you for shopping with us. Visit Again!",
                "items": existing_items,
                "grand_total": total,
                "disount": 0,
                "to_pay": total
            }
        
        with self.database_client.start_session() as session:
            try:
                # Perform operations within the transaction
                with session.start_transaction():
                    # Perform operations
                    self.order_collection.insert_one({'user_id': user_id, 'order_details': response}, session=session)
                    self.carts_collection.delete_one({'user_id': user_id}, session=session)
                # Commit the transaction
                session.commit_transaction()
                logging.info("Transaction committed successfully")

            except Exception as e:
                # Rollback the transaction if any error occurs
                session.abort_transaction()
                logging.error(f"Transaction aborted: {e}")
                raise ConnectionRefusedError('Error while writing in db!')
        
        return response, 200
