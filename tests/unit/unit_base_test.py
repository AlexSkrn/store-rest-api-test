"""This allows to have app as unused import in only one place.

As opposed to having unused app imports in all unit test files.
"""
from unittest import TestCase

from app import app


class UnitBaseTest(TestCase):
    pass
