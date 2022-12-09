import os

from elasticsearch import Elasticsearch

ELASTICSEARCH = {
    'default': Elasticsearch(
        'http://{host}:{port}'.format(
            host=os.environ['ELASTICSEARCH_HOST'],
            port=os.environ['ELASTICSEARCH_PORT'])
    )
}
