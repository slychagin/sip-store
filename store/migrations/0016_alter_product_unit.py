# Generated by Django 4.1 on 2023-03-07 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_product_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='unit',
            field=models.CharField(default='грн/кг', max_length=50, verbose_name='одиниця виміру'),
        ),
    ]