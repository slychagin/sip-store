# Generated by Django 4.1 on 2023-03-22 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SalePoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='найменування точки продажу')),
                ('description', models.TextField(blank=True, verbose_name='опис')),
                ('city', models.CharField(blank=True, max_length=100, verbose_name='місто')),
                ('street', models.CharField(blank=True, max_length=100, verbose_name='вулиця')),
                ('house', models.CharField(blank=True, max_length=10, verbose_name='будинок')),
                ('corpus', models.CharField(blank=True, max_length=10, verbose_name='корпус')),
                ('latitude', models.CharField(blank=True, max_length=50, verbose_name='широта')),
                ('longitude', models.CharField(blank=True, max_length=50, verbose_name='довгота')),
                ('mobile_phone', models.CharField(blank=True, max_length=50, verbose_name='мобільний телефон')),
                ('city_phone', models.CharField(blank=True, max_length=50, verbose_name='міський телефон')),
                ('email', models.EmailField(blank=True, max_length=100, verbose_name='E-mail')),
                ('schedule', models.CharField(blank=True, max_length=200, verbose_name='графік роботи')),
                ('image', models.ImageField(blank=True, upload_to='photos/sale_points', verbose_name='фото')),
                ('is_opened', models.BooleanField(default=True, help_text='Зняти помітку, якщо точка зачинилась або тимчасово не працює.', verbose_name='працює')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='дата замовлення')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='дата коригування')),
            ],
            options={
                'verbose_name': 'точку продажу',
                'verbose_name_plural': 'точки продажу',
                'ordering': ('created',),
            },
        ),
    ]
