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


class Partners(models.Model):
    """Create Partners model in the database"""
    objects = models.Manager()
    title = models.CharField(max_length=100, blank=True, verbose_name='Найменування партнеру')
    image = models.ImageField(upload_to='photos/partners', blank=True, verbose_name='Фото партнера')

    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнери'

    def __str__(self):
        return self.title

