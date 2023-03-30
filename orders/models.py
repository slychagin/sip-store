from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from store.models import Product


class Order(models.Model):
    """Create Order model in the database"""
    DELIVERY_METHOD_CHOICES = (
        (COURIER1 := 'COURIER_CHERKASY', _("Кур'єр по м. Черкаси")),
        (COURIER2 := 'COURIER_ZOLOTONOSHA', _("Кур'єр по м. Золотоноша")),
        (COMPANY := 'DELIVERY COMPANY', _('Доставка Новою Поштою'))
    )
    PAYMENT_METHOD_CHOICES = (
        (CASH := 'CASH', _('Готівка')),
        (TERMINAL := 'TERMINAL', _("Кур'єру через термінал")),
        (VISA := 'VISA', _('Оплата карткою VISA/MasterCard'))
    )

    phone_number_regex = RegexValidator(regex=r"^\+?1?\d{8,15}$")

    objects = models.Manager()

    order_number = models.CharField(max_length=20, verbose_name=_('номер замовлення'))
    customer_name = models.CharField(max_length=100, verbose_name=_('ПІБ'))
    phone = PhoneNumberField(validators=[phone_number_regex], max_length=16, verbose_name=_('телефон'))
    email = models.EmailField(max_length=100, verbose_name=_('E-mail'))
    city = models.CharField(max_length=50, verbose_name=_('місто'))
    street = models.CharField(max_length=50, verbose_name=_('вулиця'))
    house = models.CharField(max_length=10, verbose_name=_('будинок'))
    room = models.CharField(max_length=10, blank=True, verbose_name=_('квартира'))
    new_post_city = models.CharField(max_length=100, default='-', verbose_name=_('Місто Нової Пошти'))
    new_post_office = models.CharField(max_length=200, default='-', verbose_name=_('Відділення Нової Пошти'))
    delivery_date = models.DateField(blank=True, null=True, verbose_name=_('бажана дата доставки'))
    delivery_time = models.TimeField(blank=True, null=True, verbose_name=_('час доставки'))
    delivery_method = models.CharField(
        max_length=50, choices=DELIVERY_METHOD_CHOICES, default=COURIER1, verbose_name=_('спосіб доставки')
    )
    payment_method = models.CharField(
        max_length=50, choices=PAYMENT_METHOD_CHOICES, default=CASH, verbose_name=_('спосіб оплати')
    )
    order_note = models.TextField(max_length=255, blank=True, verbose_name=_('примітка до замовлення'))
    order_total = models.IntegerField(verbose_name=_('усього зі знижкою'))
    discount = models.IntegerField(verbose_name=_('знижка'))
    ip = models.CharField(blank=True, max_length=20, verbose_name=_('IP адреса'))
    is_ordered = models.BooleanField(default=False, verbose_name=_('замовлено'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('дата замовлення'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('дата коригування'))

    class Meta:
        verbose_name = _('замовлення')
        verbose_name_plural = _('замовлення')
        ordering = ('-created',)

    def __str__(self):
        return f'№ {self.order_number} від {self.created.date().strftime("%d.%m.%Y")}'


class OrderItem(models.Model):
    """Create OrderItem model in the database"""
    objects = models.Manager()

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_('замовлення'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('товар'))
    price = models.IntegerField(verbose_name=_('ціна товару'))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('кількість'))
    is_ordered = models.BooleanField(default=False, verbose_name=_('замовлено'))
    user_email = models.EmailField(max_length=100, verbose_name=_('E-mail'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('дата створення'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('дата оновлення'))

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = _('товар в замовленні')
        verbose_name_plural = _('товари в замовленні')
        ordering = ('-created',)


class NewPostTerminals(models.Model):
    """Create NewPostTerminals model in the database"""
    objects = models.Manager()

    city = models.CharField(max_length=100)
    terminal = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.city}, {self.terminal}'

    class Meta:
        ordering = ('city',)


class Customers(models.Model):
    """Create Customers model in the database"""
    objects = models.Manager()

    phone_number_regex = RegexValidator(regex=r"^\+?1?\d{8,15}$")

    customer_name = models.CharField(max_length=100, verbose_name=_('ПІБ'))
    phone = PhoneNumberField(validators=[phone_number_regex], max_length=16, verbose_name=_('телефон'))
    email = models.EmailField(max_length=100, verbose_name=_('E-mail'))
    note = models.TextField(blank=True, verbose_name=_('примітка'))

    def __str__(self):
        return f'{self.customer_name}'

    class Meta:
        verbose_name = _('покупця')
        verbose_name_plural = _('покупці')
        ordering = ('customer_name',)


def save_customer(order):
    """Save customer to the database"""
    customer = Customers.objects.filter(phone=order.phone).exists()
    if not customer:
        data = Customers()
        data.customer_name = order.customer_name
        data.phone = order.phone
        data.email = order.email
        data.save()


class Subscribers(models.Model):
    """Create Subscribers model in the database"""
    objects = models.Manager()

    email = models.EmailField(max_length=100, verbose_name=_('E-mail'))

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'підписчика'
        verbose_name_plural = _('підписчики')


class OrderMessage(models.Model):
    """Create OrderMessage model in the database"""
    objects = models.Manager()

    text_1 = models.TextField(
        blank=True,
        help_text=_('повідомлення між привітанням та деталями замовлення'),
        verbose_name=_('текст до деталей замовлення')
    )
    text_2 = models.TextField(
        blank=True,
        help_text=_('повідомлення після деталей замовлення'),
        verbose_name=_('текст після деталей замовлення')
    )

    class Meta:
        verbose_name = _('повідомлення покупцям')
        verbose_name_plural = _('повідомлення на email')

    def __str__(self):
        return str(_('Повідомлення покупцям на email після замовлення'))


class ThanksPage(models.Model):
    """Create ThanksPage model in the database"""
    objects = models.Manager()

    text = models.TextField(
        blank=True,
        verbose_name=_('текст до сторінки подяки')
    )

    class Meta:
        verbose_name = _('сторінка подяки')
        verbose_name_plural = _('сторінка подяки')

    def __str__(self):
        return str(_('Сторінка подяки'))
