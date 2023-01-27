# Generated by Django 4.1 on 2023-01-27 06:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0004_remove_product_is_active_product_is_new_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeekOfferBanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, verbose_name='Назва банера')),
                ('image_active', models.ImageField(upload_to='photos/banners', verbose_name='Фото 1 (активне)')),
                ('image', models.ImageField(upload_to='photos/banners', verbose_name='Фото 2')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Пропозиція тижня',
                'verbose_name_plural': 'Пропозиції тижня',
            },
        ),
    ]
