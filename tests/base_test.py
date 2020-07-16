"""
BaseTest

This class should be the parent class to each non-unit test.
It allows for instantiation of the database dynamically
and makes sure that it is a new, blank database each time.
"""

from unittest import TestCase
from app import app
from db import db

from config import TestingConfig


class BaseTest(TestCase):

    @classmethod
    def setUpClass(cls):
        """Runs once for each test case, i.e. once for entire test class."""
        # app.config['DEBUG'] = False  # Otherwise: Error: A setup function was called after the first request was handled
        # # the following config param is by default True when DEBUG is True
        # app.config['PROPAGATE_EXCEPTIONS'] = True  # otherwise, test_item_no_auth - AssertionError: 401 != 500
        # # 500 is Flask's internal server error, so that any unhandled exceptions do not give client any system info
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'  # 'postgresql://postgres:1234@localhost:5432/test'

        app.config.from_object(TestingConfig)
        with app.app_context():
            db.init_app(app)

    def setUp(self):
        """Runs once for each test method."""
        # Make sure database exists
        with app.app_context():
            db.create_all()
        # Generate a new test client every time we call self.app()
        self.app = app.test_client
        self.app_context = app.app_context

    def tearDown(self):
        # Database is blank
        with app.app_context():
            db.session.remove()
            db.drop_all()
