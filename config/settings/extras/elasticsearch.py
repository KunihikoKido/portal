import os

from elasticsearch import Elasticsearch

ELASTICSEARCH = {
    'default': {
        'client': Elasticsearch(
            'http://{host}:{port}'.format(
                host=os.environ['ELASTICSEARCH_HOST'],
                port=os.environ['ELASTICSEARCH_PORT'])
        ),
        'index_templates': (
            'elasticsearch/portal.index.template.json',
        ),
        'component_templates': (
            'elasticsearch/portal.component.template.json',
        )
    }
}
