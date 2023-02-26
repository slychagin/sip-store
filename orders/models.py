from django.core.validators import RegexValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from store.models import Product


class Order(models.Model):
    """Create Order model in the database"""
    DELIVERY_METHOD_CHOICES = (
        (COURIER := 'COURIER', "Кур'єр по м. Золотоноша та м. Черкаси"),
        (COMPANY := 'DELIVERY COMPANY', 'Доставка Новою Поштою')
    )
    PAYMENT_METHOD_CHOICES = (
        (CASH := 'CASH', 'Готівка'),
        (TERMINAL := 'TERMINAL', "Кур'єру через термінал"),
        (VISA := 'VISA', 'Оплата карткою VISA/MasterCard'),
        (GOOGLE := 'GOOGLE', 'Оплата Google Pay/Apple Pay')
    )

    phone_number_regex = RegexValidator(regex=r"^\+?1?\d{8,15}$")

    object = models.Manager()

    order_number = models.CharField(max_length=20, verbose_name='Номер замовлення')
    customer_name = models.CharField(max_length=100, verbose_name='ПІБ')
    phone = PhoneNumberField(validators=[phone_number_regex], max_length=16, verbose_name='Телефон')
    email = models.EmailField(max_length=50, verbose_name='E-mail')

    city = models.CharField(max_length=50, verbose_name='Місто')
    street = models.CharField(max_length=50, verbose_name='Вулиця')
    house = models.CharField(max_length=10, verbose_name='Будинок')
    room = models.CharField(max_length=10, blank=True, verbose_name='Квартира')

    new_post_city = models.CharField(max_length=100, default='-', verbose_name='Місто Нової Пошти')
    new_post_office = models.CharField(max_length=200, default='-', verbose_name='Відділення Нової Пошти')

    delivery_date = models.DateField(blank=True, null=True, verbose_name='Бажана дата доставки')
    delivery_time = models.TimeField(blank=True, null=True, verbose_name='Бажаний час доставки')

    delivery_method = models.CharField(max_length=50, choices=DELIVERY_METHOD_CHOICES, default=COURIER, verbose_name='Спосіб доставки')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, default=CASH, verbose_name='Спосіб оплати')

    order_note = models.TextField(max_length=255, blank=True, verbose_name='Примітка до замовлення')
    order_total = models.IntegerField(verbose_name='Усього зі знижкою')
    discount = models.IntegerField(verbose_name='Знижка')
    ip = models.CharField(blank=True, max_length=20, verbose_name='IP адреса')
    is_ordered = models.BooleanField(default=False, verbose_name='Замовлено')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
        ordering = ('-created',)

    def __str__(self):
        return f'№ {self.order_number}'


class OrderItem(models.Model):
    """Create OrderItem model in the database"""
    objects = models.Manager()

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Замовлення')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    price = models.IntegerField(verbose_name='Ціна товару')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Кількість')
    is_ordered = models.BooleanField(default=False, verbose_name='Замовлено')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'Товар в замовленні'
        verbose_name_plural = 'Товари в замовленні'
        ordering = ('-created',)


class NewPostTerminals(models.Model):
    """Create NewPostTerminals model in the database"""
    objects = models.Manager()

    city = models.CharField(max_length=100)
    terminal = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.city}, {self.terminal}'

    class Meta:
        ordering = ('city',)
