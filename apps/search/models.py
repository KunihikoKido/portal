import json

from django.conf import settings
from django.db import models
from django.template.loader import render_to_string

ELASTICSEARCH = settings.ELASTICSEARCH["default"]


class BaseSearchModel(models.Model):
    class Meta:
        abstract = True
        index_name = None
        mapping_template = None

    @classmethod
    def get_es_client(self):
        return ELASTICSEARCH["client"]

    @classmethod
    def create_index(cls):
        client = cls.get_es_client()
        return client.indices.create(
            index=cls._meta.index_name, ignore=[400, 404]
        )

    @classmethod
    def delete_index(cls):
        client = cls.get_es_client()
        return client.indices.delete(
            index=cls._meta.index_name, ignore=[400, 404]
        )

    @classmethod
    def exists_index(cls):
        client = cls.get_es_client()
        return client.indices.exists(
            index=cls._meta.index_name,
        )

    @classmethod
    def put_mapping(cls):
        client = cls.get_es_client()
        templates = json.loads(render_to_string(cls._meta.mapping_template))
        return client.indices.put_mapping(
            index=cls._meta.index_name, **templates
        )

    @classmethod
    def flush_index(cls):
        client = cls.get_es_client()
        return client.indices.flush(
            index=cls._meta.index_name,
        )

    @classmethod
    def refresh_index(cls):
        client = cls.get_es_client()
        return client.indices.refresh(
            index=cls._meta.index_name,
        )

    @classmethod
    def search(cls, query=None, **kwargs):
        client = cls.get_es_client()
        return client.search(index=cls._meta.index_name, query=query, **kwargs)

    @classmethod
    def index_document(cls, id, document, **kwargs):
        client = cls.get_es_client()
        return client.index(
            index=cls._meta.index_name, id=id, document=document, **kwargs
        )

    @classmethod
    def get_document(cls, id, **kwargs):
        client = cls.get_es_client()
        return client.get(
            index=cls._meta.index_name,
            id=id,
            **kwargs,
        )

    @classmethod
    def delete_document(cls, id, **kwargs):
        client = cls.get_es_client()
        return client.delete(index=cls._meta.index_name, id=id, **kwargs)
