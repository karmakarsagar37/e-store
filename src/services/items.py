import logging
from src.db import db_name
logging.basicConfig(level=logging.INFO)

class ItemService:
    def __init__(self, database_client) -> None:
        self.database_client = database_client
        self.database = database_client.get_database(db_name)
        self.items_collection = self.database['items']
        
    def add_items(self, item_list: list):
        items = []
        for item in item_list:
            items.append({
                '_id': item.get('item_name'),
                'item_price': item.get('item_price')
            })
        self.items_collection.insert_many(items)
        return {'success': True}, 200
        
    def get_all_items(self):
        items = self.items_collection.find({},{'_id': 1, 'item_name': 1, 'item_price': 1})
        logging.info(items)
        result = [{
            'item_name': str(item['_id']),
            'item_price': item['item_price']
            } for item in items]
        logging.info(result)
        return {
            'items': result
            }, 200