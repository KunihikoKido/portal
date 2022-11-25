import os

ELASTICSEARCH = {
    'default': {
        'client': {
            'hosts': [
                os.environ['ELASTICSEARCH_HOST'],
                os.environ['ELASTICSEARCH_HOST'],
            ],
            'port': os.environ['ELASTICSEARCH_PORT'],
            'http_auth': (
                os.environ['ELASTICSEARCH_USERNAME'],
                os.environ['ELASTICSEARCH_PASSWORD']
            ),
            'use_ssl': os.environ['ELASTICSEARCH_USE_SSL'],
            'retry_on_timeout': True,
            'timeout': 6,
        }
    }
}
