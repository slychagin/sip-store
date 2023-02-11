from django.db import models


class Coupon(models.Model):
    """Create Coupon model in the database"""
    objects = models.Manager()

    coupon_kod = models.CharField(max_length=15, verbose_name='Промокод')
    discount = models.PositiveSmallIntegerField(verbose_name='Знижка, %')
    validity = models.DateField(verbose_name='Термін дії')
    is_available = models.BooleanField(default=True, verbose_name='Знижка доступна')
    description = models.CharField(max_length=255, blank=True, verbose_name='Опис')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Дата змін')

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоди'
        ordering = ('-created_date',)

    def __str__(self):
        return self.coupon_kod
