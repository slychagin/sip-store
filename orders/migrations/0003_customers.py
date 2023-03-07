# Generated by Django 4.1 on 2023-02-27 13:42

import django.core.validators
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_order_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=100, verbose_name='ПІБ')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=16, region=None, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')], verbose_name='Телефон')),
                ('email', models.EmailField(max_length=50, verbose_name='E-mail')),
            ],
        ),
    ]