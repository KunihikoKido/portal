from django.test import TestCase as BaseTestCase

from .models import Classification


class TestCase(BaseTestCase):
    def setUp(self):
        Classification.create_index()
        Classification.put_mapping()

    def tearDown(self):
        Classification.delete_index()
