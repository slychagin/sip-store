# Generated by Django 4.1 on 2023-03-22 05:55

import django.db.models.deletion
import embed_video.fields
from django.db import migrations, models

import store.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255, verbose_name='найменування товару')),
                ('slug', models.SlugField(help_text='заповнюється автоматично, коли вносишь назву', max_length=255, unique=True, verbose_name='написання в URL')),
                ('short_description', models.TextField(blank=True, verbose_name='короткий опис')),
                ('description', models.TextField(blank=True, verbose_name='детальний опис')),
                ('specification', models.TextField(blank=True, verbose_name='специфікація')),
                ('price', models.IntegerField(verbose_name='ціна')),
                ('price_old', models.IntegerField(blank=True, null=True, verbose_name='стара ціна')),
                ('weight', models.DecimalField(blank=True, decimal_places=3, max_digits=6, null=True, verbose_name='вага, кг')),
                ('unit', models.CharField(default='грн/кг', max_length=50, verbose_name='одиниця виміру')),
                ('product_image', models.ImageField(upload_to='photos/products', verbose_name='активне фото')),
                ('second_image', models.ImageField(blank=True, help_text="Необов'язкове (потрібно для супутніх товарів)", upload_to='photos/products', verbose_name='друге фото')),
                ('is_available', models.BooleanField(default=True, verbose_name='доступний')),
                ('is_new', models.BooleanField(default=False, verbose_name='new')),
                ('is_sale', models.BooleanField(default=False, verbose_name='sale')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='дата створення')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='дата змін')),
                ('count_orders', models.IntegerField(default=0, verbose_name='замовлено одиниць')),
                ('related_products_title', models.CharField(blank='З цим товаром купують', max_length=255, verbose_name='заголовок до супутніх товарів')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='category.category', verbose_name='категорія')),
                ('related_products', models.ManyToManyField(blank=True, related_name='+', to='store.product', verbose_name='супутні товари')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'товари',
                'ordering': ('-created_date',),
            },
        ),
        migrations.CreateModel(
            name='ProductInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, verbose_name='инфо')),
            ],
            options={
                'verbose_name': 'инфо про товар',
                'verbose_name_plural': 'инфо',
            },
        ),
        migrations.CreateModel(
            name='ReviewRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField(validators=[store.models.validate_rating], verbose_name='рейтинг')),
                ('review', models.TextField(max_length=500, verbose_name='відгук')),
                ('name', models.CharField(max_length=80, verbose_name="ім'я")),
                ('email', models.EmailField(max_length=100, verbose_name='E-mail')),
                ('ip', models.CharField(blank=True, max_length=20, verbose_name='IP адреса')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='дата створення')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='дата коригування')),
                ('is_moderated', models.BooleanField(default=False, verbose_name='промодерований')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='товар')),
            ],
            options={
                'verbose_name': 'відгук',
                'verbose_name_plural': 'відгуки',
                'ordering': ('-modified_date',),
            },
        ),
        migrations.CreateModel(
            name='ProductGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, max_length=255, upload_to='photos/gallery', verbose_name='фото')),
                ('video', embed_video.fields.EmbedVideoField(blank=True, help_text='Завантаж URL відео з YouTube', verbose_name='відео')),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='товар')),
            ],
            options={
                'verbose_name': 'товар',
                'verbose_name_plural': 'галерея товарів',
            },
        ),
    ]
