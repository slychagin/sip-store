# Generated by Django 4.1 on 2023-01-26 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0004_remove_product_is_active_product_is_new_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Блок')),
            ],
            options={
                'verbose_name': 'Секція',
                'verbose_name_plural': 'Секції',
            },
        ),
        migrations.CreateModel(
            name='BestSellers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_prod1_active', models.ImageField(upload_to='photos/bestsellers', verbose_name='Фото 1')),
                ('image_prod1', models.ImageField(upload_to='photos/bestsellers', verbose_name='Фото 2')),
                ('image_prod2_active', models.ImageField(upload_to='photos/bestsellers', verbose_name='Фото 1')),
                ('image_prod2', models.ImageField(upload_to='photos/bestsellers', verbose_name='Фото 2')),
                ('product_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_1', to='store.product', verbose_name='Товар 1')),
                ('product_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_2', to='store.product', verbose_name='Товар 2')),
                ('title', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sales.blocktitle', verbose_name='Назва блоку')),
            ],
            options={
                'verbose_name': 'Бестселер',
                'verbose_name_plural': 'Бестселери',
            },
        ),
    ]
