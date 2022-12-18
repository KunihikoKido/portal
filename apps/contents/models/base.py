from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.search.models import BaseSearchModel


class BaseContent(BaseSearchModel):
    prefix_url = models.TextField(_("prefix urls"))
    is_active = models.BooleanField(_("active"), default=False)
    created = models.DateTimeField(_("created"), auto_now_add=True)
    updated = models.DateTimeField(_("updated"), auto_now=True)

    class Meta:
        abstract = True
