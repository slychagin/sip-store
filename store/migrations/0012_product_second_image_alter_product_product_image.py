# Generated by Django 4.1 on 2023-03-06 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_product_related_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='second_image',
            field=models.ImageField(blank=True, help_text="Необов'язкове (потрібно для супутніх товарів)", upload_to='photos/products', verbose_name='друге фото'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(upload_to='photos/products', verbose_name='активне фото'),
        ),
    ]
