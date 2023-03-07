# Generated by Django 4.1 on 2023-03-03 15:24

from django.db import migrations, models
import django.db.models.deletion
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
        ('store', '0005_alter_productgallery_image_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-created_date',), 'verbose_name': 'товар', 'verbose_name_plural': 'товари'},
        ),
        migrations.AlterModelOptions(
            name='productgallery',
            options={'verbose_name_plural': 'галерея товарів'},
        ),
        migrations.AddField(
            model_name='product',
            name='short_description',
            field=models.TextField(blank=True, verbose_name='короткий опис'),
        ),
        migrations.AddField(
            model_name='product',
            name='specification',
            field=models.TextField(blank=True, verbose_name='специфікація'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='category.category', verbose_name='категорія'),
        ),
        migrations.AlterField(
            model_name='product',
            name='count_orders',
            field=models.IntegerField(default=0, verbose_name='замовлено одиниць'),
        ),
        migrations.AlterField(
            model_name='product',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='дата створення'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, verbose_name='детальний опис'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_available',
            field=models.BooleanField(default=True, verbose_name='доступний'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_new',
            field=models.BooleanField(default=False, verbose_name='new'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_sale',
            field=models.BooleanField(default=False, verbose_name='sale'),
        ),
        migrations.AlterField(
            model_name='product',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, verbose_name='дата змін'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(verbose_name='ціна'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_old',
            field=models.IntegerField(blank=True, null=True, verbose_name='стара ціна'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(upload_to='photos/products', verbose_name='фото товару'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(max_length=255, verbose_name='найменування товару'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='product',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=6, null=True, verbose_name='вага, кг'),
        ),
        migrations.AlterField(
            model_name='productgallery',
            name='image',
            field=models.ImageField(blank=True, max_length=255, upload_to='photos/gallery', verbose_name='фото'),
        ),
        migrations.AlterField(
            model_name='productgallery',
            name='product',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='товар'),
        ),
        migrations.AlterField(
            model_name='productgallery',
            name='video',
            field=embed_video.fields.EmbedVideoField(blank=True, help_text='Завантаж URL відео з YouTube', verbose_name='відео'),
        ),
    ]