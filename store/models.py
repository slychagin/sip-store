from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from embed_video.fields import EmbedVideoField

from category.models import Category


class Product(models.Model):
    """Create Product model in the database"""
    objects = models.Manager()
    product_name = models.CharField(max_length=255, verbose_name=_('найменування товару'))
    slug = models.SlugField(max_length=255, unique=True, verbose_name=_('написання в URL'), help_text=_('заповнюється автоматично, коли вносишь назву'))
    short_description = models.TextField(blank=True, verbose_name=_('короткий опис'))
    description = models.TextField(blank=True, verbose_name=_('детальний опис'))
    specification = models.TextField(blank=True, verbose_name=_('специфікація'))
    price = models.IntegerField(verbose_name=_('ціна'))
    price_old = models.IntegerField(blank=True, null=True, verbose_name=_('стара ціна'))
    weight = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True, verbose_name=_('вага, кг'))
    unit = models.CharField(max_length=50, default='грн/кг', verbose_name=_('одиниця виміру'))
    product_image = models.ImageField(upload_to='photos/products', verbose_name=_('активне фото'))
    second_image = models.ImageField(
        upload_to='photos/products',
        blank=True,
        help_text=_("Необов'язкове (потрібно для супутніх товарів)"),
        verbose_name=_('друге фото')
    )
    is_available = models.BooleanField(default=True, verbose_name=_('доступний'))
    is_new = models.BooleanField(default=False, verbose_name=_('new'))
    is_sale = models.BooleanField(default=False, verbose_name=_('sale'))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('дата створення'))
    modified_date = models.DateTimeField(auto_now=True, verbose_name=_('дата змін'))
    count_orders = models.IntegerField(default=0, verbose_name=_('замовлено одиниць'))
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, verbose_name=_('категорія'))
    related_products_title = models.CharField(max_length=255, blank='З цим товаром купують', verbose_name=_('заголовок до супутніх товарів'))
    related_products = models.ManyToManyField('self', related_name='+', symmetrical=False, blank=True, verbose_name=_('супутні товари'))

    class Meta:
        verbose_name = _('товар')
        verbose_name_plural = _('товари')
        ordering = ('-created_date',)

    def __str__(self):
        return self.product_name

    def get_url(self):
        """Get product url to go to product detail page"""
        return reverse('product_details', args=[self.category.slug, self.slug])

    def average_review_rating(self):
        """Calculate average review rating for particular product"""
        reviews = ReviewRating.objects.filter(product=self, is_moderated=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = round(float(reviews['average']), 2)
            if (avg - int(avg)) >= 0.5:
                avg = int(avg) + 0.5
            else:
                avg = float(int(avg))
        return avg


def count_products(basket):
    """Save qty to product count orders"""
    for item in basket:
        product = Product.objects.get(id=item['product'].pk)
        product.count_orders += item['qty']
        product.save()


class ProductGallery(models.Model):
    objects = models.Manager()
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE, verbose_name=_('товар'))
    image = models.ImageField(blank=True, upload_to='photos/gallery', max_length=255, verbose_name=_('фото'))
    video = EmbedVideoField(blank=True, verbose_name=_('відео'), help_text=_('Завантаж URL відео з YouTube'))

    def __str__(self):
        return f'{self.product.product_name}'

    class Meta:
        verbose_name = _('товар')
        verbose_name_plural = _('галерея товарів')


class ProductInfo(models.Model):
    """Create ProductInfo model in the database"""
    objects = models.Manager()
    description = models.TextField(blank=True, verbose_name=_('инфо'))

    class Meta:
        verbose_name = _('инфо про товар')
        verbose_name_plural = _('инфо')

    def __str__(self):
        return 'Інформація щодо товару'


def validate_rating(value):
    """
    Check rating that in should be from 0.5 to 5.0
    with step 0.5
    """
    rating_list = [x / 10.0 for x in range(5, 55, 5)]
    if value not in rating_list:
        raise ValidationError(
            _('Рейтинг повинен входити до діапазону від 0,5 до 5,0 з кроком 0,5')
        )


class ReviewRating(models.Model):
    """Create ReviewRating model in the database"""
    objects = models.Manager()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('товар'))
    rating = models.FloatField(validators=[validate_rating], verbose_name=_('рейтинг'))
    review = models.TextField(max_length=500, verbose_name=_('відгук'))
    name = models.CharField(max_length=80, verbose_name=_("ім'я"))
    email = models.EmailField(max_length=100, verbose_name=_('E-mail'))
    ip = models.CharField(max_length=20, blank=True, verbose_name=_('IP адреса'))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_('дата створення'))
    modified_date = models.DateTimeField(auto_now=True, verbose_name=_('дата коригування'))
    is_moderated = models.BooleanField(default=False, verbose_name=_('промодерований'))

    class Meta:
        verbose_name = _('відгук')
        verbose_name_plural = _('відгуки')
        ordering = ('-modified_date',)

    def __str__(self):
        return f'{self.product.product_name}'


