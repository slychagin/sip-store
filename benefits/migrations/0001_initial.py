# Generated by Django 4.1 on 2023-02-22 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Benefits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, verbose_name='Заголовок')),
                ('description', models.CharField(blank=True, max_length=255, verbose_name='Опис')),
                ('image', models.ImageField(blank=True, upload_to='photos/benefits', verbose_name='Фото переваги')),
            ],
            options={
                'verbose_name': 'Перевага',
                'verbose_name_plural': 'Переваги',
            },
        ),
        migrations.CreateModel(
            name='Partners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, verbose_name='Найменування партнеру')),
                ('image', models.ImageField(blank=True, upload_to='photos/partners', verbose_name='Фото партнера')),
            ],
            options={
                'verbose_name': 'Партнер',
                'verbose_name_plural': 'Партнери',
            },
        ),
    ]
