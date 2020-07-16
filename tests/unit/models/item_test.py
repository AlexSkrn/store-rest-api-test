from unittest import TestCase

from models.item import ItemModel

from tests.unit.unit_base_test import UnitBaseTest
# from models.store import StoreModel  # needed to run but unused

# from tests.base_test import BaseTest


class ItemTest(UnitBaseTest):  # TestCase, BaseCase
    def test_create_item(self):
        # with self.app_context():  # added to fix 'either push context' etc error related to using the database
        #     StoreModel('test').save_to_db()  # this creates store with id 1 for tests to work with Postgres
        item = ItemModel('test', 19.99, 1)

        self.assertEqual(item.name, 'test',
                         "The name of the item after creation does not equal the constructor argument.")
        self.assertEqual(item.price, 19.99,
                         "The price of the item after creation does not equal the constructor argument.")

        self.assertEqual(item.store_id, 1)

        self.assertIsNone(item.store)

    def test_item_json(self):
        # with self.app_context():
        #     StoreModel('test').save_to_db()  # this creates store with id 1 for tests to work with Postgres
        item = ItemModel('test', 19.99, 1)
        expected = {
            'name': 'test',
            'price': 19.99
        }

        self.assertEqual(
            item.json(),
            expected,
            "The JSON export of the item is incorrect. Received {}, expected {}.".format(item.json(), expected))
