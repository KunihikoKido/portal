from django.test import TestCase as BaseTestCase

from .models import ProductDocument


class TestCase(BaseTestCase):
    def setUp(self):
        exists = ProductDocument.exists_index()
        if not exists:
            ProductDocument.create_index()
            ProductDocument.put_mapping()

    def tearDown(self):
        exists = ProductDocument.exists_index()
        if exists:
            ProductDocument.delete_index()
