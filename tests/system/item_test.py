import json

from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel

from tests.base_test import BaseTest


def context_decorator(func):
    def return_function(self):
        with self.app() as client:
            with self.app_context():
                func(self, client)
    return return_function


class ItemTest(BaseTest):

    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                # create a user first to be able to log in
                UserModel('test', '1234').save_to_db()
                auth_response = client.post(
                    '/auth',
                    data=json.dumps(
                        {'username': 'test',
                         'password': '1234'
                         }
                        ),
                    headers={'Content-Type':
                             'application/json'
                             }
                    )
                auth_token = json.loads(
                    auth_response.data
                    )['access_token']
                self.access_token = f'JWT {auth_token}'

    @context_decorator
    def test_item_no_auth(self, client):
        # with self.app() as client:
        #     with self.app_context():
        resp = client.get('/item/test')
        self.assertEqual(
            401,  # this code *_may_* also come from @app.errorhandler(JWTError) in app.py
            resp.status_code
        )

    @context_decorator
    def test_get_item_not_found(self, client):
        # with self.app() as client:
        #     with self.app_context():
        resp = client.get(
             'item/test',
             headers={'Authorization': self.access_token}
             )

        self.assertEqual(404, resp.status_code)

    @context_decorator
    def test_get_item(self, client):
        # with self.app() as client:
        #     with self.app_context():
        StoreModel('test').save_to_db()
        ItemModel('test', 19.99, 1).save_to_db()
        resp = client.get(
             'item/test',
             headers={'Authorization': self.access_token}
             )

        self.assertEqual(200, resp.status_code)
        self.assertEqual(
            {'name': 'test',
             'price': 19.99},
            json.loads(resp.data)
             )

    @context_decorator
    def test_delete_item(self, client):
        # with self.app() as client:
        #     with self.app_context():
        StoreModel('test').save_to_db()
        ItemModel('test', 19.99, 1).save_to_db()

        resp = client.delete(
             'item/test',
             # headers={'Authorization': self.access_token}
             )
        self.assertEqual(200, resp.status_code)
        self.assertDictEqual(
            {'message': 'Item deleted'},
            json.loads(resp.data)
        )

    @context_decorator
    def test_create_item(self, client):
        # with self.app() as client:
        #     with self.app_context():
        StoreModel('test').save_to_db()

        resp = client.post(
             'item/test',
             data={'name': 'test',
                   'price': 19.99,
                   'store_id': 1
                   }
             )
        self.assertEqual(201, resp.status_code)
        self.assertDictEqual(
            {'name': 'test', 'price': 19.99},
            json.loads(resp.data)
        )

    @context_decorator
    def test_create_duplicate_item(self, client):
        # with self.app() as client:
        #     with self.app_context():
        StoreModel('test').save_to_db()
        ItemModel('test', 19.99, 1).save_to_db()

        resp = client.post(
             'item/test',
             data={'name': 'test',
                   'price': 19.99,
                   'store_id': 1
                   }
             )
        self.assertEqual(400, resp.status_code)
        self.assertDictEqual(
            {'message':
             "An item with name 'test' already exists."},
            json.loads(resp.data)
        )

    @context_decorator
    def test_put_item(self, client):
        # with self.app() as client:
        #     with self.app_context():
        StoreModel('test').save_to_db()

        resp = client.put(
             'item/test',
             data={'name': 'test',
                   'price': 19.99,
                   'store_id': 1
                   }
             )
        self.assertEqual(200, resp.status_code)
        self.assertDictEqual(
            {'name': 'test', 'price': 19.99},
            json.loads(resp.data)
        )
        self.assertEqual(
            19.99,
            ItemModel.find_by_name('test').price
            )

    @context_decorator
    def test_put_update_item(self, client):
        # with self.app() as client:
        #     with self.app_context():
        StoreModel('test').save_to_db()
        ItemModel('test', 19.99, 1).save_to_db()

        self.assertEqual(
            19.99,
            ItemModel.find_by_name('test').price
            )

        resp = client.put(
             'item/test',
             data={'name': 'test',
                   'price': 10.99,
                   'store_id': 1
                   }
             )
        self.assertEqual(200, resp.status_code)
        self.assertDictEqual(
            {'name': 'test', 'price': 10.99},
            json.loads(resp.data)
        )
        self.assertEqual(
            10.99,
            ItemModel.find_by_name('test').price
            )

    @context_decorator
    def test_item_list(self, client):
        # with self.app() as client:
        #     with self.app_context():
        StoreModel('test').save_to_db()
        ItemModel('test', 19.99, 1).save_to_db()

        resp = client.get('/items')

        self.assertEqual(200, resp.status_code)

        self.assertDictEqual(
            {'items':
             [{'name': 'test', 'price': 19.99}]
             },
            json.loads(resp.data)
        )
