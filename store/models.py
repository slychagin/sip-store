from django.db import models
from category.models import Category


class Product(models.Model):
    """Create Product model in the database"""
    objects = models.Manager()

    product_name = models.CharField(max_length=255, verbose_name='Найменування товару')
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, verbose_name='Опис')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Ціна')
    product_image = models.ImageField(upload_to='photos/products', verbose_name='Фото товару')
    is_available = models.BooleanField(default=True, verbose_name='Доступний')
    is_active = models.BooleanField(default=True, verbose_name='Активний')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Дата змін')
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, verbose_name='Категорія')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'
        ordering = ('-created_date',)

    def __str__(self):
        return self.product_name
