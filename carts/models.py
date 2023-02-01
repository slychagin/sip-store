from django.db import models

from store.models import Product


class Cart(models.Model):
    """Create Cart model in the database"""
    objects = models.Manager()
    cart_id = models.CharField(max_length=255, blank=True, verbose_name='ID кошика')
    date_added = models.DateField(auto_now_add=True, verbose_name='Дата додавання')

    def __str__(self):
        return self.cart_id

    class Meta:
        verbose_name = 'Кошик'
        verbose_name_plural = 'Кошики'


class CartItem(models.Model):
    """Create CartItem model in the database"""
    objects = models.Manager()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, verbose_name='Кошик')
    quantity = models.IntegerField(verbose_name='Кількість')
    is_active = models.BooleanField(default=True, verbose_name='Активно')

    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product

    class Meta:
        verbose_name = 'Товар у кошику'
        verbose_name_plural = 'Товари у кошику'
