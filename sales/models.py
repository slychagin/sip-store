from django.db import models
from django.utils.translation import gettext_lazy as _

from store.models import Product


class BlockTitle(models.Model):
    """Create block titles for sales blocks"""
    objects = models.Manager()

    title = models.CharField(max_length=100, verbose_name=_('назва блоку'))

    class Meta:
        verbose_name = _('блок')
        verbose_name_plural = _('блоки')

    def __str__(self):
        return self.title


class BestSellers(models.Model):
    """Create BestSellers model in the database"""
    objects = models.Manager()

    title = models.ForeignKey(BlockTitle, on_delete=models.SET_NULL, null=True, verbose_name=_('назва блоку'))
    product_1 = models.ForeignKey(
        Product, related_name='product_1', on_delete=models.CASCADE, verbose_name=_('товар 1')
    )
    image_prod1_active = models.ImageField(upload_to='photos/bestsellers', verbose_name=_('фото 1 (активне)'))
    image_prod1 = models.ImageField(upload_to='photos/bestsellers', verbose_name=_('фото 2'))

    product_2 = models.ForeignKey(
        Product, related_name='product_2', on_delete=models.CASCADE, verbose_name=_('товар 2')
    )
    image_prod2_active = models.ImageField(upload_to='photos/bestsellers', verbose_name=_('фото 1 (активне)'))
    image_prod2 = models.ImageField(upload_to='photos/bestsellers', verbose_name=_('фото 2'))

    class Meta:
        verbose_name = _('бестселер')
        verbose_name_plural = _('бестселери')

    def __str__(self):
        return f'Секція: {self.product_1}, {self.product_2}'


class NewProducts(models.Model):
    """Create NewProducts model in the database"""
    objects = models.Manager()

    title = models.ForeignKey(BlockTitle, on_delete=models.SET_NULL, null=True, verbose_name=_('назва блоку'))
    product_1 = models.ForeignKey(
        Product, related_name='new_product_1', on_delete=models.CASCADE, verbose_name=_('товар 1')
    )
    image_prod1_active = models.ImageField(upload_to='photos/new_products', verbose_name=_('фото 1 (активне)'))
    image_prod1 = models.ImageField(upload_to='photos/new_products', verbose_name=_('фото 2'))

    product_2 = models.ForeignKey(
        Product, related_name='new_product_2', on_delete=models.CASCADE, verbose_name=_('товар 2')
    )
    image_prod2_active = models.ImageField(upload_to='photos/new_products', verbose_name=_('фото 1 (активне)'))
    image_prod2 = models.ImageField(upload_to='photos/new_products', verbose_name=_('фото 2'))

    class Meta:
        verbose_name = _('новинка')
        verbose_name_plural = _('новинки')

    def __str__(self):
        return f'Секція: {self.product_1}, {self.product_2}'


class MostPopularLeft(models.Model):
    """Create MostPopular model in the database"""
    objects = models.Manager()

    title = models.ForeignKey(BlockTitle, on_delete=models.SET_NULL, null=True, verbose_name=_('назва блоку'))

    product_1 = models.ForeignKey(
        Product, related_name='pop_product_1', on_delete=models.CASCADE, verbose_name=_('товар 1')
    )
    image_prod1_active = models.ImageField(upload_to='photos/popular_products', verbose_name=_('фото 1 (активне)'))
    image_prod1 = models.ImageField(upload_to='photos/popular_products', verbose_name=_('фото 2'))

    product_2 = models.ForeignKey(
        Product, related_name='pop_product_2', on_delete=models.CASCADE, verbose_name=_('товар 2')
    )
    image_prod2_active = models.ImageField(upload_to='photos/popular_products', verbose_name=_('фото 1 (активне)'))
    image_prod2 = models.ImageField(upload_to='photos/popular_products', verbose_name=_('фото 2'))

    product_3 = models.ForeignKey(
        Product, related_name='pop_product_3', on_delete=models.CASCADE, verbose_name=_('товар 3')
    )
    image_prod3_active = models.ImageField(upload_to='photos/popular_products', verbose_name=_('фото 1 (активне)'))
    image_prod3 = models.ImageField(upload_to='photos/popular_products', verbose_name=_('фото 2'))

    class Meta:
        verbose_name = _('популярний (ліворуч)')
        verbose_name_plural = _('популярні (ліворуч)')

    def __str__(self):
        return f'Секція: {self.product_1}, {self.product_2}, {self.product_3}'


class MostPopularCenter(models.Model):
    """Create MostPopularCenter model in the database"""
    objects = models.Manager()

    title = models.ForeignKey(BlockTitle, on_delete=models.SET_NULL, null=True, verbose_name=_('назва блоку'))

    product_1 = models.ForeignKey(
        Product, related_name='pop_center_product_1', on_delete=models.CASCADE, verbose_name=_('товар 1')
    )
    image_prod1_active = models.ImageField(upload_to='photos/popular_products', verbose_name=_('фото 1 (активне)'))
    image_prod1 = models.ImageField(upload_to='photos/popular_products', verbose_name=_('фото 2'))

    product_2 = models.ForeignKey(
        Product, related_name='pop_center_product_2', on_delete=models.CASCADE, verbose_name=_('товар 2')
    )
    image_prod2_active = models.ImageField(upload_to='photos/popular_products', verbose_name=_('фото 1 (активне)'))
    image_prod2 = models.ImageField(upload_to='photos/popular_products', verbose_name=_('фото 2'))

    product_3 = models.ForeignKey(
        Product, related_name='pop_center_product_3', on_delete=models.CASCADE, verbose_name=_('товар 3')
    )
    image_prod3_active = models.ImageField(upload_to='photos/popular_products', verbose_name=_('фото 1 (активне)'))
    image_prod3 = models.ImageField(upload_to='photos/popular_products', verbose_name=_('фото 2'))

    class Meta:
        verbose_name = _('популярний (по центру)')
        verbose_name_plural = _('популярні (по центру)')

    def __str__(self):
        return f'Секція: {self.product_1}, {self.product_2}, {self.product_3}'


class MostPopularRight(models.Model):
    """Create MostPopularRight model in the database"""
    objects = models.Manager()

    title = models.ForeignKey(BlockTitle, on_delete=models.SET_NULL, null=True, verbose_name=_('назва блоку'))

    product_1 = models.ForeignKey(
        Product, related_name='pop_right_product_1', on_delete=models.CASCADE, verbose_name=_('товар 1')
    )
    image_prod1_active = models.ImageField(upload_to='photos/popular_products', verbose_name=_('фото 1 (активне)'))
    image_prod1 = models.ImageField(upload_to='photos/popular_products', verbose_name=_('фото 2'))

    product_2 = models.ForeignKey(
        Product, related_name='pop_right_product_2', on_delete=models.CASCADE, verbose_name=_('товар 2')
    )
    image_prod2_active = models.ImageField(upload_to='photos/popular_products', verbose_name=_('фото 1 (активне)'))
    image_prod2 = models.ImageField(upload_to='photos/popular_products', verbose_name=_('фото 2'))

    product_3 = models.ForeignKey(
        Product, related_name='pop_right_product_3', on_delete=models.CASCADE, verbose_name=_('товар 3')
    )
    image_prod3_active = models.ImageField(upload_to='photos/popular_products', verbose_name=_('фото 1 (активне)'))
    image_prod3 = models.ImageField(upload_to='photos/popular_products', verbose_name=_('фото 2'))

    class Meta:
        verbose_name = _('популярний (праворуч)')
        verbose_name_plural = _('популярні (праворуч)')

    def __str__(self):
        return f'Секція: {self.product_1}, {self.product_2}, {self.product_3}'
