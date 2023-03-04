from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BenefitsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'benefits'
    verbose_name = _('переваги')
