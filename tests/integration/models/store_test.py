from models.store import StoreModel
from models.item import ItemModel

from tests.base_test import BaseTest


class StoreTest(BaseTest):

    def test_create_store_items_empty(self):
        store = StoreModel(name='test')

        self.assertListEqual(
            store.items.all(),
            [],
            'Store items length not 0 though no items were added.'
            )

    def test_crud(self):
        """Test writing to, and deleting from, the db."""
        with self.app_context():
            store = StoreModel(name='test')

            self.assertIsNone(StoreModel.find_by_name('test'))

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name('test'))

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name('test'))

    def test_store_relationship_with_item(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test item', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)  # instead of .all()
            self.assertEqual(store.items.first().name, 'test item')
            # store.items.first() is a StoreModel object

    def test_store_json(self):
        store = StoreModel('test')
        expected = {
            'id': None,  # I don't save store to db, so id is not generated
            'name': 'test',
            'items': []
        }

        self.assertDictEqual(store.json(), expected)

    def test_store_json_with_item(self):
        with self.app_context():   # Note the differnce with the prev. test!
            store = StoreModel('test')
            item = ItemModel('test item', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            expected = {
                'id': 1,
                'name': 'test',
                'items': [{'name': 'test item', 'price': 19.99}]
            }

            self.assertDictEqual(store.json(), expected)
