import json
import os

from django.apps import AppConfig
from django.conf import settings
from django.template.loader import render_to_string

ELASTICSEARCH = settings.ELASTICSEARCH['default']


def get_templates(name=None):
    templates = ELASTICSEARCH[name]
    for template_name in templates:
        name, _ = os.path.splitext(os.path.basename(template_name))
        template = json.loads(render_to_string(template_name))
        yield name, template


class SearchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'search'

    def ready(self):
        client = ELASTICSEARCH['client']
        for name, params in get_templates(name='component_templates'):
            client.cluster.put_component_template(name=name, **params)

        for name, params in get_templates(name='index_templates'):
            client.indices.put_index_template(name=name, **params)
