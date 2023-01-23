from django.db import models


class Category(models.Model):
    """Create Category model in the database"""
    objects = models.Manager()

    category_name = models.CharField(max_length=100, unique=True, verbose_name='Найменування категорії')
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, verbose_name='Опис')
    category_image = models.ImageField(upload_to='photos/categories', blank=True, verbose_name='Фото категорії')

    class Meta:
        verbose_name = 'Категорію'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.category_name
