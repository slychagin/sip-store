from django.db import models

from store.models import Product


class BlockTitle(models.Model):
    """Create block titles for sales blocks"""
    objects = models.Manager()
    title = models.CharField(max_length=100, verbose_name='Назва блоку')

    class Meta:
        verbose_name = 'Блок'
        verbose_name_plural = 'Блоки'

    def __str__(self):
        return self.title


class BestSellers(models.Model):
    """Create BestSellers model in the database"""
    objects = models.Manager()

    title = models.ForeignKey(BlockTitle, on_delete=models.SET_NULL, null=True, verbose_name='Назва блоку')
    product_1 = models.ForeignKey(Product, related_name='product_1', on_delete=models.CASCADE, verbose_name='Товар 1')
    image_prod1_active = models.ImageField(upload_to='photos/bestsellers', verbose_name='Фото 1 (активне)')
    image_prod1 = models.ImageField(upload_to='photos/bestsellers', verbose_name='Фото 2')
    product_2 = models.ForeignKey(Product,  related_name='product_2', on_delete=models.CASCADE, verbose_name='Товар 2')
    image_prod2_active = models.ImageField(upload_to='photos/bestsellers', verbose_name='Фото 1 (активне)')
    image_prod2 = models.ImageField(upload_to='photos/bestsellers', verbose_name='Фото 2')

    class Meta:
        verbose_name = 'Бестселер'
        verbose_name_plural = 'Бестселери'

    def __str__(self):
        return f'Секція: {self.product_1}, {self.product_2}'


class NewProducts(models.Model):
    """Create NewProducts model in the database"""
    objects = models.Manager()

    title = models.ForeignKey(BlockTitle, on_delete=models.SET_NULL, null=True, verbose_name='Назва блоку')
    product_1 = models.ForeignKey(Product, related_name='new_product_1', on_delete=models.CASCADE, verbose_name='Товар 1')
    image_prod1_active = models.ImageField(upload_to='photos/new_products', verbose_name='Фото 1 (активне)')
    image_prod1 = models.ImageField(upload_to='photos/new_products', verbose_name='Фото 2')
    product_2 = models.ForeignKey(Product,  related_name='new_product_2', on_delete=models.CASCADE, verbose_name='Товар 2')
    image_prod2_active = models.ImageField(upload_to='photos/new_products', verbose_name='Фото 1 (активне)')
    image_prod2 = models.ImageField(upload_to='photos/new_products', verbose_name='Фото 2')

    class Meta:
        verbose_name = 'Новинка'
        verbose_name_plural = 'Новинки'

    def __str__(self):
        return f'Секція: {self.product_1}, {self.product_2}'








