from django.test import TestCase as BaseTestCase

from apps.classifications.models import Classification
from apps.documents.models import ProductDocument


class TestCase(BaseTestCase):
    def setUp(self):
        ProductDocument.create_index()
        ProductDocument.put_mapping()
        Classification.create_index()
        Classification.put_mapping()

    def tearDown(self):
        Classification.delete_index()
        ProductDocument.delete_index()
