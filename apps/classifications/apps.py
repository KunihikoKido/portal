from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ClassificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.classifications"
    verbose_name = _("classifications")

    def ready(self):
        from .models import Classification

        Classification.create_index()
        Classification.put_mapping()
