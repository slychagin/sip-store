# Generated by Django 4.1 on 2023-02-10 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='discount',
            field=models.PositiveSmallIntegerField(verbose_name='Знижка, %'),
        ),
    ]