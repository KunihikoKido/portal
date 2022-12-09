from django.test import TestCase

from ..models import Classification
from ..serializers import ClassificationQuerySerializer


class ClassificationQuerySerializerTest(TestCase):
    def setUp(self):
        self.classification = Classification(
            id=1,
            slug='sightseeing',
            name='観光ツアー',
            order=2,
            classification_type='category',
            synonyms="世界遺産\n半日観光\n\n",
            antonyms="空港送迎"
        )
        self.classification.save()

    def test_serializing(self):
        serializer = ClassificationQuerySerializer(
            instance=self.classification)
        self.assertEqual(
            serializer.data,
            {
                "id": "classification-1",
                "query": {
                    'bool': {
                        'should': [
                            {'match_phrase': {'_all': '観光ツアー'}},
                            {'match_phrase': {'_all': '世界遺産'}},
                            {'match_phrase': {'_all': '半日観光'}}
                        ],
                        'minimum_should_match': '1',
                        'must_not': [
                            {'match_phrase': {'_all': '空港送迎'}}
                        ]
                    }
                },
                "classification_meta": {
                    "slug": "sightseeing",
                    "name": "観光ツアー",
                    "order": 2,
                    "classification_type": "category",
                    "key": "000002≠sightseeing≠観光ツアー"
                }
            }
        )
