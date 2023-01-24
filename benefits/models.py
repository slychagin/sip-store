from django.db import models


class Benefits(models.Model):
    """Create Benefits model in the database"""
    objects = models.Manager()

    title = models.CharField(max_length=100, blank=True, verbose_name='Заголовок')
    description = models.CharField(max_length=255, blank=True, verbose_name='Опис')
    image = models.ImageField(upload_to='photos/benefits', blank=True, verbose_name='Фото переваги')

    class Meta:
        verbose_name = 'Перевага'
        verbose_name_plural = 'Переваги'

    def __str__(self):
        return self.title
