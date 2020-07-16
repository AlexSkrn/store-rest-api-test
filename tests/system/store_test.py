import json

from models.store import StoreModel
from models.item import ItemModel
from tests.base_test import BaseTest


class TestStore(BaseTest):

    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                resp = client.post(
                    '/store/test'
                    )

                self.assertIsNotNone(
                    StoreModel.find_by_name('test')
                )
                self.assertEqual(201, resp.status_code)
                self.assertDictEqual(
                    {'id': 1,
                     'name': 'test',
                     'items': []
                     },
                    json.loads(resp.data)
                    )

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    '/store/test'
                    )
                resp = client.post(
                    '/store/test'
                    )
                expected = {'message':
                            "A store with name 'test' already exists."
                            }
                self.assertDictEqual(
                    expected,
                    json.loads(resp.data)
                )
                self.assertEqual(400, resp.status_code)

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    '/store/test'
                    )
                # alternatively:
                # StoreModel('test').save_to_db()

                self.assertIsNotNone(
                    StoreModel.find_by_name('test')
                )
                resp = client.delete('/store/test')
                self.assertIsNone(
                    StoreModel.find_by_name('test')
                )
                self.assertDictEqual(
                    json.loads(resp.data),
                    {'message': 'Store deleted'}
                )
                self.assertEqual(200, resp.status_code)

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    '/store/test'
                    )

                resp = client.get('/store/test')
                self.assertEqual(200, resp.status_code)
                self.assertDictEqual(
                    {'id': 1,
                     'name': 'test',
                     'items': []
                     },
                    json.loads(resp.data)
                    )

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/store/test')
                self.assertEqual(404, resp.status_code)  # most clients will not look into data after 404
                self.assertDictEqual(
                    {'message': 'Store not found'},
                    json.loads(resp.data)
                    )

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    '/store/test'
                    )
                # client.post(
                #     '/item/test',
                #     data={'name': 'test',
                #           'price': 10.99,
                #           'store_id': 1
                #           }
                #     )
                ItemModel('test', 19.99, 1).save_to_db()

                resp = client.get('/store/test')
                self.assertEqual(200, resp.status_code)
                self.assertDictEqual(
                    {'id': 1,
                     'name': 'test',
                     'items': [{'name': 'test',
                                'price': 19.99,
                                # 'store_id': 1
                                }
                               ]
                     },
                     json.loads(resp.data)

                    )

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    '/store/test'
                    )

                resp = client.get('/stores')
                self.assertEqual(200, resp.status_code)
                self.assertDictEqual(
                    {'stores': [{'id': 1,
                                 'name': 'test',
                                 'items': []
                                 }
                                ]
                     },
                    json.loads(resp.data)

                )

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    '/store/test'
                    )
                ItemModel('test', 19.99, 1).save_to_db()

                resp = client.get('/stores')
                self.assertEqual(200, resp.status_code)
                self.assertDictEqual(
                    {'stores': [{'id': 1,
                                 'name': 'test',
                                 'items': [{'name': 'test',
                                            'price': 19.99
                                            }
                                           ]
                                 }
                                ]
                     },
                    json.loads(resp.data)
                )
