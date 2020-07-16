from models.store import StoreModel

from tests.unit.unit_base_test import UnitBaseTest


class StoreTest(UnitBaseTest):

    def test_store_creation(self):
        store = StoreModel(name='test')

        self.assertEqual(store.name, 'test')
