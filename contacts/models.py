from django.db import models
from django.utils.translation import gettext_lazy as _


class SalePoint(models.Model):
    """Create SalePoint model in the database"""
    objects = models.Manager()

    name = models.CharField(max_length=200, unique=True, verbose_name=_('найменування точки продажу'))
    description = models.TextField(blank=True, null=True, verbose_name=_('опис'))

    city = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('місто'))
    street = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('вулиця'))
    house = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('будинок'))
    corpus = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('корпус'))
    latitude = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('широта'))
    longitude = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('довгота'))

    mobile_phone = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('мобільний телефон'))
    city_phone = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('міський телефон'))
    email = models.EmailField(max_length=100, blank=True, null=True, verbose_name=_('E-mail'))

    schedule = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('графік роботи'))

    image = models.ImageField(upload_to='photos/sale_points', blank=True, null=True, verbose_name=_('фото'))
    is_opened = models.BooleanField(default=True, verbose_name=_('працює'),
                                    help_text=_('Зняти помітку, якщо точка зачинилась або тимчасово не працює.'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('дата замовлення'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('дата коригування'))

    class Meta:
        verbose_name = _('точку продажу')
        verbose_name_plural = _('точки продажу')
        ordering = ('-created',)

    def __str__(self):
        return self.name
