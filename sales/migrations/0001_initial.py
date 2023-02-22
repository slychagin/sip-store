# Generated by Django 4.1 on 2023-02-22 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Назва блоку')),
            ],
            options={
                'verbose_name': 'Блок',
                'verbose_name_plural': 'Блоки',
            },
        ),
        migrations.CreateModel(
            name='NewProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_prod1_active', models.ImageField(upload_to='photos/new_products', verbose_name='Фото 1 (активне)')),
                ('image_prod1', models.ImageField(upload_to='photos/new_products', verbose_name='Фото 2')),
                ('image_prod2_active', models.ImageField(upload_to='photos/new_products', verbose_name='Фото 1 (активне)')),
                ('image_prod2', models.ImageField(upload_to='photos/new_products', verbose_name='Фото 2')),
                ('product_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_product_1', to='store.product', verbose_name='Товар 1')),
                ('product_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_product_2', to='store.product', verbose_name='Товар 2')),
                ('title', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sales.blocktitle', verbose_name='Назва блоку')),
            ],
            options={
                'verbose_name': 'Новинка',
                'verbose_name_plural': 'Новинки',
            },
        ),
        migrations.CreateModel(
            name='MostPopularRight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_prod1_active', models.ImageField(upload_to='photos/popular_products', verbose_name='Фото 1 (активне)')),
                ('image_prod1', models.ImageField(upload_to='photos/popular_products', verbose_name='Фото 2')),
                ('image_prod2_active', models.ImageField(upload_to='photos/popular_products', verbose_name='Фото 1 (активне)')),
                ('image_prod2', models.ImageField(upload_to='photos/popular_products', verbose_name='Фото 2')),
                ('image_prod3_active', models.ImageField(upload_to='photos/popular_products', verbose_name='Фото 1 (активне)')),
                ('image_prod3', models.ImageField(upload_to='photos/popular_products', verbose_name='Фото 2')),
                ('product_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pop_right_product_1', to='store.product', verbose_name='Товар 1')),
                ('product_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pop_right_product_2', to='store.product', verbose_name='Товар 2')),
                ('product_3', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pop_right_product_3', to='store.product', verbose_name='Товар 3')),
                ('title', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sales.blocktitle', verbose_name='Назва блоку')),
            ],
            options={
                'verbose_name': 'Популярний (праворуч)',
                'verbose_name_plural': 'Популярні (праворуч)',
            },
        ),
        migrations.CreateModel(
            name='MostPopularLeft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_prod1_active', models.ImageField(upload_to='photos/popular_products', verbose_name='Фото 1 (активне)')),
                ('image_prod1', models.ImageField(upload_to='photos/popular_products', verbose_name='Фото 2')),
                ('image_prod2_active', models.ImageField(upload_to='photos/popular_products', verbose_name='Фото 1 (активне)')),
                ('image_prod2', models.ImageField(upload_to='photos/popular_products', verbose_name='Фото 2')),
                ('image_prod3_active', models.ImageField(upload_to='photos/popular_products', verbose_name='Фото 1 (активне)')),
                ('image_prod3', models.ImageField(upload_to='photos/popular_products', verbose_name='Фото 2')),
                ('product_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pop_product_1', to='store.product', verbose_name='Товар 1')),
                ('product_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pop_product_2', to='store.product', verbose_name='Товар 2')),
                ('product_3', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pop_product_3', to='store.product', verbose_name='Товар 3')),
                ('title', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sales.blocktitle', verbose_name='Назва блоку')),
            ],
            options={
                'verbose_name': 'Популярний (ліворуч)',
                'verbose_name_plural': 'Популярні (ліворуч)',
            },
        ),
        migrations.CreateModel(
            name='MostPopularCenter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_prod1_active', models.ImageField(upload_to='photos/popular_products', verbose_name='Фото 1 (активне)')),
                ('image_prod1', models.ImageField(upload_to='photos/popular_products', verbose_name='Фото 2')),
                ('image_prod2_active', models.ImageField(upload_to='photos/popular_products', verbose_name='Фото 1 (активне)')),
                ('image_prod2', models.ImageField(upload_to='photos/popular_products', verbose_name='Фото 2')),
                ('image_prod3_active', models.ImageField(upload_to='photos/popular_products', verbose_name='Фото 1 (активне)')),
                ('image_prod3', models.ImageField(upload_to='photos/popular_products', verbose_name='Фото 2')),
                ('product_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pop_center_product_1', to='store.product', verbose_name='Товар 1')),
                ('product_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pop_center_product_2', to='store.product', verbose_name='Товар 2')),
                ('product_3', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pop_center_product_3', to='store.product', verbose_name='Товар 3')),
                ('title', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sales.blocktitle', verbose_name='Назва блоку')),
            ],
            options={
                'verbose_name': 'Популярний (по центру)',
                'verbose_name_plural': 'Популярні (по центру)',
            },
        ),
        migrations.CreateModel(
            name='BestSellers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_prod1_active', models.ImageField(upload_to='photos/bestsellers', verbose_name='Фото 1 (активне)')),
                ('image_prod1', models.ImageField(upload_to='photos/bestsellers', verbose_name='Фото 2')),
                ('image_prod2_active', models.ImageField(upload_to='photos/bestsellers', verbose_name='Фото 1 (активне)')),
                ('image_prod2', models.ImageField(upload_to='photos/bestsellers', verbose_name='Фото 2')),
                ('product_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_1', to='store.product', verbose_name='Товар 1')),
                ('product_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_2', to='store.product', verbose_name='Товар 2')),
                ('title', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sales.blocktitle', verbose_name='Назва блоку')),
            ],
            options={
                'verbose_name': 'Бестселер',
                'verbose_name_plural': 'Бестселери',
            },
        ),
    ]
