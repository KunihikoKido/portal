from django.apps import AppConfig


class DocumentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.documents'

    def ready(self):
        from .models import ProductDocument
        ProductDocument.create_index()
        ProductDocument.put_mapping()
