from apps.search.test import TestCase

from ..models import Classification
from ..serializers import ClassificationPercolatorSerializer


class ClassificationPercolatorTest(TestCase):
    def setUp(self):
        super().setUp()
        self.classification = Classification(
            id=1,
            slug="sightseeing",
            name="観光ツアー",
            order=2,
            classification_type="category",
            synonyms="世界遺産\n半日観光\n\n",
            antonyms="空港送迎",
        )
        self.classification.save()
        self.percolator = {
            "query": {
                "bool": {
                    "should": [
                        {"match_phrase": {"_all": "sightseeing"}},
                        {"match_phrase": {"_all": "観光ツアー"}},
                        {"match_phrase": {"_all": "世界遺産"}},
                        {"match_phrase": {"_all": "半日観光"}},
                    ],
                    "minimum_should_match": "1",
                    "must_not": [{"match_phrase": {"_all": "空港送迎"}}],
                }
            },
            "_meta": {
                "classification": {
                    "slug": "sightseeing",
                    "name": "観光ツアー",
                    "order": 2,
                    "classification_type": "category",
                    "key": "000002≠sightseeing≠観光ツアー",
                }
            },
        }

    def test_serializer(self):
        percolator = ClassificationPercolatorSerializer(
            instance=self.classification
        ).data
        percolator.pop("id")
        self.assertEqual(self.percolator, percolator)

    def test_index_percolator(self):
        percolator = ClassificationPercolatorSerializer(
            instance=self.classification
        ).data
        doc_id = percolator.pop("id")
        Classification.index_document(
            id=doc_id,
            document=percolator,
        )
        response = Classification.get_document(id=doc_id)
        self.assertEqual(percolator, response["_source"])

    def test_match_percolate_query(self):
        percolator = ClassificationPercolatorSerializer(
            instance=self.classification
        ).data
        doc_id = percolator.pop("id")
        Classification.index_document(
            id=doc_id,
            document=percolator,
        )
        Classification.refresh_index()
        response = Classification.search(
            query={
                "percolate": {
                    "field": "query",
                    "document": {"title": "ハワイ一周島内観光ツアー"},
                },
            },
            source_includes=["_meta"],
        )

        # Response hits total value
        self.assertEqual(1, response["hits"]["total"]["value"])

        # Response metadata
        self.assertEqual(
            {
                "slug": "sightseeing",
                "name": "観光ツアー",
                "order": 2,
                "classification_type": "category",
                "key": "000002≠sightseeing≠観光ツアー",
            },
            response["hits"]["hits"][0]["_source"]["_meta"]["classification"],
        )

    def test_not_match_percolate_query(self):
        percolator = ClassificationPercolatorSerializer(
            instance=self.classification
        ).data
        doc_id = percolator.pop("id")
        Classification.index_document(
            id=doc_id,
            document=percolator,
        )
        Classification.refresh_index()
        response = Classification.search(
            query={
                "percolate": {
                    "field": "query",
                    "document": {"title": "沖縄の海でダイビング初心者歓迎"},
                }
            },
            source_includes=["_meta"],
        )

        # Response hits total value
        self.assertEqual(0, response["hits"]["total"]["value"])
