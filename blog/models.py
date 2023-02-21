from django.db import models
from django.urls import reverse

from store.models import Product


class BlogCategory(models.Model):
    """Create BlogCategory in the database"""
    objects = models.Manager()

    category_name = models.CharField(max_length=100, unique=True, verbose_name='Найменування категорії')
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, verbose_name='Опис')
    category_image = models.ImageField(upload_to='photos/blog', blank=True, verbose_name='Фото категорії')

    class Meta:
        verbose_name = 'Категорію'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.category_name

    def get_url(self):
        """
        Get blog category url to use in right side navbar menu
        :return: url for particular blog category
        """
        return reverse('posts_by_category', args=[self.slug])


class Tag(models.Model):
    """Create Tag model in the database"""
    objects = models.Manager()

    name = models.CharField(max_length=100, verbose_name='Назва тегу')
    product = models.ForeignKey(Product, related_name='product', on_delete=models.CASCADE, verbose_name='Продукт')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Post(models.Model):
    """Create Post model in the database"""
    objects = models.Manager()

    title = models.CharField(max_length=255, verbose_name='Тема поста')
    description = models.TextField(blank=True, verbose_name='Опис поста')
    quote = models.TextField(blank=True, verbose_name='Цитата до посту')
    post_image = models.ImageField(upload_to='photos/blog/images', blank=True, verbose_name='Фото до посту')
    mini_image = models.ImageField(upload_to='photos/blog/mini_images', verbose_name='Міні фото до посту')
    is_available = models.BooleanField(default=True, verbose_name='Доступний')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Дата змін')
    post_category = models.ForeignKey(BlogCategory, related_name='post', on_delete=models.CASCADE, verbose_name='Категорія')
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Пости'
        ordering = ('-created_date',)

    def __str__(self):
        return self.title

    def get_url(self):
        """
        Get blog url to go to blog details page.
        :return: reverse url for particular blog
        """
        return reverse('post_details', args=[self.post_category.slug, self.pk])

    def post_created_date(self):
        """Get just date from created date (without time)"""
        return self.created_date.date()

    def recent_created_date(self):
        """Modified created date to format dd/mm/yyyy"""
        return self.created_date.date().strftime('%d/%m/%Y')
