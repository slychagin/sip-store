# Generated by Django 4.1 on 2023-03-06 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banners', '0002_mainbanner_alter_weekofferbanner_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TwoBanners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, verbose_name='заголовок')),
                ('image', models.ImageField(upload_to='photos/banners', verbose_name='фото')),
                ('banner_url', models.URLField(max_length=255, verbose_name='URL банера')),
            ],
            options={
                'verbose_name': 'банер',
                'verbose_name_plural': 'банери (2шт.)',
            },
        ),
        migrations.AlterModelOptions(
            name='mainbanner',
            options={'verbose_name': 'головний банер', 'verbose_name_plural': 'головні банери'},
        ),
        migrations.AlterModelOptions(
            name='weekofferbanner',
            options={'verbose_name': 'пропозицію тижня', 'verbose_name_plural': 'пропозиції тижня'},
        ),
    ]