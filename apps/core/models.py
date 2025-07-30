from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("created time"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("updated time"))

    class Meta:
        abstract = True
