from django.db import models
from django.utils.translation import gettext_lazy as _


class TelegramSettings(models.Model):
    """Create TelegramSettings model in the database"""
    tg_token = models.CharField(max_length=100, verbose_name=_('токен'))
    tg_chat = models.CharField(max_length=100, verbose_name=_('чат ID'))
    tg_api = models.CharField(max_length=100, verbose_name=_('API адреса'))
    tg_message = models.TextField(blank=True, verbose_name=_('текст повідомлення'))
    available = models.BooleanField(default=True, verbose_name=_('активний'))

    objects = models.Manager()

    def __str__(self):
        return self.tg_chat

    class Meta:
        verbose_name_plural = _('налаштування')
