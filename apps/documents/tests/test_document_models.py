from apps.search.test import TestCase

from ..models import ProductDocument


class DocumentModelTest(TestCase):
    def test_create_index(self):
        ProductDocument.delete_index()
        response = ProductDocument.create_index()
        self.assertEqual(True, response["acknowledged"])

    def test_delete_index(self):
        response = ProductDocument.delete_index()
        self.assertEqual(True, response["acknowledged"])

    def test_exists_index(self):
        response = ProductDocument.exists_index()
        self.assertEqual(True, response)

    def test_put_mapping(self):
        response = ProductDocument.put_mapping()
        self.assertEqual(True, response["acknowledged"])

    def test_flush_index(self):
        response = ProductDocument.flush_index()
        self.assertEqual(
            {"_shards": {"total": 1, "successful": 1, "failed": 0}},
            response,
        )

    def test_refresh_index(self):
        response = ProductDocument.refresh_index()
        self.assertEqual(
            {"_shards": {"total": 1, "successful": 1, "failed": 0}},
            response,
        )

    def test_search(self):
        ProductDocument.index_document(
            id=1,
            document={"title": "Hello World!"},
        )
        ProductDocument.refresh_index()
        response = ProductDocument.search(query={"match_all": {}})
        self.assertEqual(1, response["hits"]["total"]["value"])

    def test_index_document(self):
        doc_id = 1
        document = {"title": "Hello World!"}
        ProductDocument.index_document(id=doc_id, document=document)
        response = ProductDocument.get_document(id=doc_id)
        self.assertEqual(document, response["_source"])

    def test_delete_document(self):
        doc_id = 1
        document = {"title": "Hello World!"}
        ProductDocument.index_document(id=doc_id, document=document)
        response = ProductDocument.delete_document(id=doc_id)
        self.assertEqual("deleted", response["result"])
