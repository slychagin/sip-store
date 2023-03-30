from django.db import models
from django.utils.translation import gettext_lazy as _

from store.models import Product


class WeekOfferBanner(models.Model):
    """Create Week Offer Banner model for left banner in the database"""
    objects = models.Manager()

    title = models.CharField(max_length=100, blank=True, verbose_name=_('назва банера'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('товар'))
    image_active = models.ImageField(upload_to='photos/banners', verbose_name=_('фото 1 (активне)'))
    image = models.ImageField(upload_to='photos/banners', verbose_name=_('фото 2'))
    countdown = models.DateField(blank=True, null=True, verbose_name=_('таймер'))

    class Meta:
        verbose_name = _('пропозицію тижня')
        verbose_name_plural = _('пропозиції тижня')

    def __str__(self):
        return self.title


class MainBanner(models.Model):
    """Create Main Banner model in the database"""
    objects = models.Manager()

    title = models.CharField(max_length=200, blank=True, verbose_name=_('заголовок'))
    description = models.CharField(max_length=255, blank=True, verbose_name=_('опис'))
    image = models.ImageField(upload_to='photos/banners', verbose_name=_('фото'))
    banner_url = models.URLField(max_length=255, verbose_name=_('URL банера'))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('дата створення'))
    modified_date = models.DateTimeField(auto_now=True, verbose_name=_('дата коригування'))

    class Meta:
        verbose_name = _('головний банер')
        verbose_name_plural = _('головні банери')
        ordering = ('-modified_date',)

    def __str__(self):
        return str(_('Банер'))


class TwoBanners(models.Model):
    """Create TwoBanners model in the database"""
    objects = models.Manager()

    title = models.CharField(max_length=100, blank=True, verbose_name=_('заголовок'))
    image = models.ImageField(upload_to='photos/banners', verbose_name=_('фото'), help_text=_('розмір фото 561х190'))
    banner_url = models.URLField(max_length=255, verbose_name=_('URL банера'))

    class Meta:
        verbose_name = _('банер')
        verbose_name_plural = _('банери (2од.)')

    def __str__(self):
        return self.title


class OfferSingleBanner(models.Model):
    """Create OfferSingleBanner model in the database"""
    objects = models.Manager()

    image = models.ImageField(upload_to='photos/banners', verbose_name=_('фото'))
    banner_url = models.URLField(max_length=255, verbose_name=_('URL банера'))

    class Meta:
        verbose_name = _('банер')
        verbose_name_plural = _('банер (1од.)')

    def __str__(self):
        return str(_('Одиночний банер зліва'))


class FooterBanner(models.Model):
    """Create FooterBanner model in the database"""
    objects = models.Manager()

    image = models.ImageField(upload_to='photos/banners', verbose_name=_('фото'), help_text=_('розмір фото 1146х240'))
    banner_url = models.URLField(max_length=255, verbose_name=_('URL банера'))

    class Meta:
        verbose_name = _('банер')
        verbose_name_plural = _('футер банер')

    def __str__(self):
        return str(_('Футер банер'))


class BackgroundBanner(models.Model):
    """Create BackgroundBanner model in the database"""
    objects = models.Manager()

    image = models.ImageField(upload_to='photos/banners', verbose_name=_('фото'))
    banner_url = models.URLField(max_length=255, blank=True, verbose_name=_('URL банера'))

    class Meta:
        verbose_name = _('фоновий банер')
        verbose_name_plural = _('фоновий банер')

    def __str__(self):
        return str(_('Фоновий банер'))
