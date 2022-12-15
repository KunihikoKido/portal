from apps.search.test import TestCase

from ..models import Classification
from ..serializers import ClassificationRuleSerializer


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
        self.classification_rule = {
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

    def test_classification_rule_serializer(self):
        classification_rule = ClassificationRuleSerializer(
            instance=self.classification
        ).data
        classification_rule.pop("id")
        self.assertEqual(self.classification_rule, classification_rule)

    def test_index_classification_rule(self):
        classification_rule = ClassificationRuleSerializer(
            instance=self.classification
        ).data
        doc_id = classification_rule.pop("id")
        Classification.index_document(
            id=doc_id,
            document=classification_rule,
        )
        response = Classification.get_document(id=doc_id)
        self.assertEqual(classification_rule, response["_source"])

    def test_match_classification_rule_query(self):
        classification_rule = ClassificationRuleSerializer(
            instance=self.classification
        ).data
        doc_id = classification_rule.pop("id")
        Classification.index_document(
            id=doc_id,
            document=classification_rule,
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

    def test_not_match_classification_rule_query(self):
        classification_rule = ClassificationRuleSerializer(
            instance=self.classification
        ).data
        doc_id = classification_rule.pop("id")
        Classification.index_document(
            id=doc_id,
            document=classification_rule,
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
