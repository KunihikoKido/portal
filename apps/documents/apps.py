from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DocumentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.documents"
    verbose_name = _("documents")

    def ready(self):
        from .models import ProductDocument

        ProductDocument.create_index()
        ProductDocument.put_mapping()
