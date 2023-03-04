from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BannersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'banners'
    verbose_name = _('банери')
