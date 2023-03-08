from django.db import models
from django.utils.translation import gettext_lazy as _


class Coupon(models.Model):
    """Create Coupon model in the database"""
    objects = models.Manager()
    coupon_kod = models.CharField(max_length=15, verbose_name=_('промокод'))
    discount = models.PositiveSmallIntegerField(verbose_name=_('знижка, %'))
    validity = models.DateField(verbose_name=_('термін дії'))
    is_available = models.BooleanField(default=True, verbose_name=_('знижка доступна'))
    description = models.CharField(max_length=255, blank=True, verbose_name=_('опис'))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('дата створення'))
    modified_date = models.DateTimeField(auto_now=True, verbose_name=_('дата змін'))

    class Meta:
        verbose_name = _('промокод')
        verbose_name_plural = _('промокоди')
        ordering = ('-created_date',)

    def __str__(self):
        return self.coupon_kod
