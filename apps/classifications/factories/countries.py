import factory

from ..models import CountryClassification


class CountryClassificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CountryClassification
        exclude = (
            "synonyms_keywords",
            "antonyms_keywords",
        )

    slug = factory.Faker("slug")
    name = factory.Faker("country")
    order = factory.Faker("random_number")

    synonyms_keywords = factory.Faker("words", nb=5)
    synonyms = factory.LazyAttribute(
        lambda obj: "\n".join(obj.synonyms_keywords)
    )

    antonyms_keywords = factory.Faker("words", nb=5)
    antonyms = factory.LazyAttribute(
        lambda obj: "\n".join(obj.antonyms_keywords)
    )
