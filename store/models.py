from django.db import models
from django.urls import reverse

from category.models import Category


class Product(models.Model):
    """Create Product model in the database"""
    objects = models.Manager()

    product_name = models.CharField(max_length=255, verbose_name='Найменування товару')
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, verbose_name='Опис')
    price = models.IntegerField(verbose_name='Ціна')
    price_old = models.IntegerField(blank=True, null=True, verbose_name='Стара ціна')
    weight = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, verbose_name='Вага, кг')
    product_image = models.ImageField(upload_to='photos/products', verbose_name='Фото товару')
    is_available = models.BooleanField(default=True, verbose_name='Доступний')
    is_new = models.BooleanField(default=False, verbose_name='New')
    is_sale = models.BooleanField(default=False, verbose_name='Sale')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Дата змін')
    count_orders = models.IntegerField(default=0, verbose_name='Замовлено одиниць')
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, verbose_name='Категорія')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'
        ordering = ('-created_date',)

    def __str__(self):
        return self.product_name

    def get_url(self):
        """
        Get product url to go to product detail page.
        :return: reverse url for particular product
        """
        return reverse('product_details', args=[self.category.slug, self.slug])


def count_products(basket):
    """Save qty to product count orders"""
    for item in basket:
        product = Product.objects.get(id=item['product'].pk)
        product.count_orders += item['qty']
        product.save()
