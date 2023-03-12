# Generated by Django 4.1 on 2023-03-12 07:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_alter_productgallery_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField(verbose_name='рейтинг')),
                ('review', models.TextField(blank=True, max_length=500, verbose_name='відгук')),
                ('name', models.CharField(max_length=80, verbose_name="ім'я")),
                ('email', models.EmailField(max_length=100, verbose_name='E-mail')),
                ('ip', models.CharField(blank=True, max_length=20, verbose_name='IP адреса')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='дата створення')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='дата коригування')),
                ('is_moderated', models.BooleanField(default=False, verbose_name='промодерований')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='товар')),
            ],
            options={
                'verbose_name': 'відгук',
                'verbose_name_plural': 'відгуки',
                'ordering': ('-modified_date',),
            },
        ),
    ]
