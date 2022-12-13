import json

import django.db.models.options as model_options
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string

ELASTICSEARCH = settings.ELASTICSEARCH["default"]

model_options.DEFAULT_NAMES += (
    "index_name",
    "mapping_template",
    "elasticsearch",
)


class BaseSearchModel(models.Model):
    class Meta:
        abstract = True
        index_name = None
        mapping_template = None
        elasticsearch = None

    @classmethod
    def create_index(cls):
        return cls._meta.elasticsearch.indices.create(
            index=cls._meta.index_name, ignore=[400, 404]
        )

    @classmethod
    def delete_index(cls):
        return cls._meta.elasticsearch.indices.delete(
            index=cls._meta.index_name, ignore=[400, 404]
        )

    @classmethod
    def exists_index(cls):
        return cls._meta.elasticsearch.indices.exists(
            index=cls._meta.index_name,
        )

    @classmethod
    def put_mapping(cls):
        templates = json.loads(render_to_string(cls._meta.mapping_template))
        return cls._meta.elasticsearch.indices.put_mapping(
            index=cls._meta.index_name, **templates
        )

    @classmethod
    def flush_index(cls):
        return cls._meta.elasticsearch.indices.flush(
            index=cls._meta.index_name,
        )

    @classmethod
    def refresh_index(cls):
        return cls._meta.elasticsearch.indices.refresh(
            index=cls._meta.index_name,
        )

    @classmethod
    def search(cls, query=None, **kwargs):
        return cls._meta.elasticsearch.search(
            index=cls._meta.index_name, query=query, **kwargs
        )

    @classmethod
    def index_document(cls, id, document, **kwargs):
        return cls._meta.elasticsearch.index(
            index=cls._meta.index_name, id=id, document=document, **kwargs
        )

    @classmethod
    def get_document(cls, id, **kwargs):
        return cls._meta.elasticsearch.get(
            index=cls._meta.index_name,
            id=id,
            **kwargs,
        )

    @classmethod
    def delete_document(cls, id, **kwargs):
        return cls._meta.elasticsearch.delete(
            index=cls._meta.index_name, id=id, **kwargs
        )
