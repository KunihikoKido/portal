# Generated by Django 4.1.4 on 2022-12-08 09:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True, verbose_name='slug')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='order')),
                ('classification_type', models.CharField(choices=[('category', 'Sub Category'), ('region', 'Region'), ('country', 'Country'), ('city', 'City')], default='category', max_length=20, verbose_name='classification type')),
                ('synonyms', models.TextField(blank=True, help_text='The clause (query) should appear in the matching documents.', verbose_name='synonyms')),
                ('antonyms', models.TextField(blank=True, help_text='The clause (query) must not appear in the matching documents.', verbose_name='antonyms')),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='ProductDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(unique=True, verbose_name='url')),
                ('title', models.CharField(blank=True, max_length=100, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('image_url', models.URLField(blank=True, verbose_name='image url')),
                ('pub_date', models.DateTimeField(db_index=True, default=django.utils.timezone.now, help_text='Set the date and time you want your post to be published.', verbose_name='publication date')),
                ('is_active', models.BooleanField(default=False, help_text='Designates whether this article should be treated as active. Unselect this instead of deleting articles.', verbose_name='active')),
                ('product_id', models.CharField(blank=True, max_length=100, verbose_name='product id')),
                ('brand_name', models.CharField(blank=True, max_length=100, verbose_name='brand name')),
                ('offer_count', models.IntegerField(blank=True, null=True, verbose_name='offer count')),
                ('low_price', models.IntegerField(blank=True, null=True, verbose_name='low price')),
                ('high_price', models.IntegerField(blank=True, null=True, verbose_name='high price')),
                ('price_currency', models.CharField(blank=True, max_length=100, verbose_name='price currency')),
                ('rating', models.FloatField(verbose_name='review rating')),
                ('review_count', models.IntegerField(blank=True, null=True, verbose_name='review count')),
                ('category_classifications', models.ManyToManyField(blank=True, limit_choices_to={'classification_type': 'category'}, related_name='CategoryProductDocument', to='documents.classification', verbose_name='category classifications')),
                ('city_classifications', models.ManyToManyField(blank=True, limit_choices_to={'classification_type': 'city'}, related_name='CityProductDocument', to='documents.classification', verbose_name='city classifications')),
                ('country_classifications', models.ManyToManyField(blank=True, limit_choices_to={'classification_type': 'country'}, related_name='CountryProductDocument', to='documents.classification', verbose_name='country classifications')),
                ('region_classifications', models.ManyToManyField(blank=True, limit_choices_to={'classification_type': 'region'}, related_name='RegionProductDocument', to='documents.classification', verbose_name='region classifications')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
