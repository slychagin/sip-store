from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """Create Category model in the database"""
    objects = models.Manager()

    category_name = models.CharField(max_length=100, unique=True, verbose_name=_('найменування категорії'))
    slug = models.SlugField(
        max_length=255, unique=True, verbose_name=_('написання в URL'),
        help_text=_('заповнюється автоматично, коли вносишь назву')
    )
    description = models.TextField(blank=True, verbose_name=_('опис'))
    category_image = models.ImageField(
        upload_to='photos/categories', blank=True, verbose_name=_('фото категорії')
    )

    class Meta:
        verbose_name = _('категорію')
        verbose_name_plural = _('категорії')

    def __str__(self):
        return self.category_name

    def get_url(self):
        """Get category url to use in navbar menu"""
        return reverse('products_by_category', args=[self.slug])
