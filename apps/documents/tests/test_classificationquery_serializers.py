from apps.documents.models import Classification
from apps.documents.serializers import ClassificationQuerySerializer
from django.test import TestCase


class ClassificationQuerySerializerTest(TestCase):
    def setUp(self):
        self.classification = Classification(
            id=1,
            slug='sightseeing',
            name='観光ツアー',
            order=0,
            classification_type='category',
            language="ja",
            synonyms="世界遺産ツアー\n半日観光",
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
                            {'match_phrase': {'_all': '世界遺産ツアー'}},
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
                    "order": 0,
                    "classification_type": "category",
                    "language": "ja"
                }
            }
        )
