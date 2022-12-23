# Generated by Django 4.1 on 2022-12-18 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefix_url', models.TextField(verbose_name='prefix urls')),
                ('is_active', models.BooleanField(default=False, verbose_name='active')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='updated')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('link', models.URLField(verbose_name='link')),
                ('start_datetime', models.DateTimeField(verbose_name='start datetime')),
                ('end_datetime', models.DateTimeField(verbose_name='end datetime')),
            ],
            options={
                'verbose_name': 'recommendation',
                'verbose_name_plural': 'recommendations',
                'index_name': 'portal.contents.recommendations',
                'mapping_template': 'mappings/portal.contents.recommendation.json',
            },
        ),
    ]