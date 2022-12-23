import factory
from django.utils.timezone import utc

from ..models import ProductDocument


class ProductDocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductDocument
        django_get_or_create = ("url",)

    url = factory.Faker("uri")
    title = factory.Faker("sentence", nb_words=10)
    description = factory.Faker("paragraph", nb_sentences=5)
    image_url = factory.Faker("image_url", width=1024, height=768)
    pub_date = factory.Faker("date_time_this_year", tzinfo=utc)
    is_active = factory.Faker("boolean", chance_of_getting_true=75)
    product_id = factory.Faker(
        "bothify",
        text="????-########",
        letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    )
    brand_name = factory.Faker("company")
    offer_count = factory.Faker("random_number")
    low_price = factory.Faker("randomize_nb_elements", number=1000, le=True)
    high_price = factory.Faker("randomize_nb_elements", number=1000, ge=True)
    price_currency = "JPY"
    rating = factory.Faker(
        "pyfloat",
        min_value=0.0,
        max_value=5.0,
        right_digits=1,
    )
    review_count = factory.Faker("random_number")
