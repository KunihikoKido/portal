from django.test import TestCase as BaseTestCase

from .models import Classification


class TestCase(BaseTestCase):
    def setUp(self):
        exists = Classification.exists_index()
        if not exists:
            Classification.create_index()
            Classification.put_mapping()

    def tearDown(self):
        exists = Classification.exists_index()
        if exists:
            Classification.delete_index()
