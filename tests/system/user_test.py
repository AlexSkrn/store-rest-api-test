import json

from models.user import UserModel
from tests.base_test import BaseTest


class UserTest(BaseTest):

    def test_register_user(self):
        # because we want to send requests to our app we need:
        with self.app() as client:
            # because our methods save data to db we also need:
            with self.app_context():
                response = client.post(
                    '/register',
                    data={'username': 'test',
                          'password': 1234
                          }  # this dict gets converted into json when request is sent
                    )  # this is recieved by post method of UserRegister

                self.assertEqual(response.status_code, 201)
                self.assertDictEqual(
                    {'message': 'User create successfully'},
                    json.loads(response.data)  # convert json object into Python object
                    )
                self.assertIsNotNone(
                    UserModel.find_by_username('test')
                    )


    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    '/register',
                    data={'username': 'test',
                          'password': '1234'
                          }
                    )

                auth_response = client.post(
                    '/auth',  # does not accept data in Form format, requires json
                    data=json.dumps(
                        {'username': 'test',
                         'password': '1234'
                         }
                        ),
                    headers={'Content-Type': 'application/json'}
                    )
                self.assertIn(
                    'access_token',
                    json.loads(auth_response.data).keys()
                    )

    def test_register_duplicate_user_fails(self):
        with self.app() as client:
            with self.app_context():
                client.post(
                    '/register',
                    data={'username': 'test',
                          'password': '1234'
                          }
                    )
                response = client.post(
                    '/register',
                    data={'username': 'test',
                          'password': '1234'
                          }
                    )
                self.assertDictEqual(
                    {'message': 'A user with such name already exists'},
                    json.loads(response.data)
                )
                self.assertEqual(
                    response.status_code,
                    400
                    )
