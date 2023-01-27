from django.db import models

from store.models import Product


class WeekOfferBanner(models.Model):
    """Create Week Offer model for left banner"""
    objects = models.Manager()

    title = models.CharField(max_length=100, blank=True, verbose_name='Назва банера')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    image_active = models.ImageField(upload_to='photos/banners', verbose_name='Фото 1 (активне)')
    image = models.ImageField(upload_to='photos/banners', verbose_name='Фото 2')

    class Meta:
        verbose_name = 'Пропозиція тижня'
        verbose_name_plural = 'Пропозиції тижня'

    def __str__(self):
        return self.title












# class TwoBanners(models.Model):
#     """Create TwoBanners model in the database"""
#     objects = models.Manager()
#
#     title = models.CharField(max_length=100, blank=True, verbose_name='Заголовок')
#     description = models.CharField(max_length=255, blank=True, verbose_name='Опис')
#     image = models.ImageField(upload_to='photos/banners', blank=True, verbose_name='Фото банеру')
#
#     class Meta:
#         verbose_name_plural = 'Банери (2шт.)'
#
#     def __str__(self):
#         return self.title

