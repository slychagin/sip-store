# Generated by Django 4.1 on 2023-01-26 09:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bestsellers',
            name='image_prod1_active',
            field=models.ImageField(upload_to='photos/bestsellers', verbose_name='Фото 1 (активне)'),
        ),
        migrations.AlterField(
            model_name='bestsellers',
            name='image_prod2_active',
            field=models.ImageField(upload_to='photos/bestsellers', verbose_name='Фото 1 (активне)'),
        ),
        migrations.AlterField(
            model_name='bestsellers',
            name='title',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sales.blocktitle', verbose_name='Назва блоку'),
        ),
        migrations.AlterField(
            model_name='blocktitle',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Назва блоку'),
        ),
    ]
