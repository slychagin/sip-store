from django.db import models
from django.utils.translation import gettext_lazy as _


class Benefits(models.Model):
    """Create Benefits model in the database"""
    objects = models.Manager()

    title = models.CharField(max_length=100, blank=True, verbose_name=_('заголовок'))
    description = models.CharField(max_length=255, blank=True, verbose_name=_('опис'))
    image = models.ImageField(upload_to='photos/benefits', blank=True, verbose_name=_('фото переваги'))

    class Meta:
        verbose_name = _('перевагу')
        verbose_name_plural = _('переваги')

    def __str__(self):
        return self.title


class Partners(models.Model):
    """Create Partners model in the database"""
    objects = models.Manager()

    title = models.CharField(max_length=100, blank=True, verbose_name=_('найменування партнера'))
    image = models.ImageField(upload_to='photos/partners', blank=True, verbose_name=_('фото партнера'))

    class Meta:
        verbose_name = _('партнер')
        verbose_name_plural = _('партнери')

    def __str__(self):
        return self.title

