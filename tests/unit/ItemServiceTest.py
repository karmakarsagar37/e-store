import unittest
from unittest.mock import MagicMock

from src.services.items import ItemService


class TestItemService(unittest.TestCase):
    def setUp(self):
        self.mock_db_client = MagicMock()
        self.item_service = ItemService(self.mock_db_client)
        self.mock_collection = self.mock_db_client.get_database.return_value.__getitem__.return_value

    def test_add_items(self):
        # Prepare test data
        test_items = [
            {'item_name': 'Item1', 'item_price': 10},
            {'item_name': 'Item2', 'item_price': 20}
        ]

        # Call the method to test
        self.item_service.add_items(test_items)

        # Assertions
        self.mock_collection.insert_many.assert_called_once()

    def test_get_all_items(self):
        # Prepare mocked data
        mocked_items = [
            {'_id': 'Item1', 'item_price': 10},
            {'_id': 'Item2', 'item_price': 20}
        ]
        self.mock_collection.find.return_value = mocked_items

        # Call the method to test
        response = self.item_service.get_all_items()

        # Assertions
        self.assertEqual(response[1], 200)  # Check status code
        self.assertEqual(len(response[0]['items']), len(mocked_items))  # Check if items are retrieved

    # Add more test cases as needed...

if __name__ == '__main__':
    unittest.main()
