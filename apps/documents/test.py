from django.test import TestCase as BaseTestCase

from .models import ProductDocument


class TestCase(BaseTestCase):
    def setUp(self):
        ProductDocument.create_index()
        ProductDocument.put_mapping()

    def tearDown(self):
        ProductDocument.delete_index()
