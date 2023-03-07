# Generated by Django 4.1 on 2023-03-07 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('benefits', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='benefits',
            options={'verbose_name': 'перевага', 'verbose_name_plural': 'переваги'},
        ),
        migrations.AlterModelOptions(
            name='partners',
            options={'verbose_name': 'партнер', 'verbose_name_plural': 'партнери'},
        ),
        migrations.AlterField(
            model_name='benefits',
            name='description',
            field=models.CharField(blank=True, max_length=255, verbose_name='опис'),
        ),
        migrations.AlterField(
            model_name='benefits',
            name='image',
            field=models.ImageField(blank=True, upload_to='photos/benefits', verbose_name='фото переваги'),
        ),
        migrations.AlterField(
            model_name='benefits',
            name='title',
            field=models.CharField(blank=True, max_length=100, verbose_name='заголовок'),
        ),
        migrations.AlterField(
            model_name='partners',
            name='image',
            field=models.ImageField(blank=True, upload_to='photos/partners', verbose_name='фото партнера'),
        ),
        migrations.AlterField(
            model_name='partners',
            name='title',
            field=models.CharField(blank=True, max_length=100, verbose_name='найменування партнеру'),
        ),
    ]