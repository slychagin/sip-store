# Generated by Django 4.1 on 2023-03-12 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_alter_reviewrating_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewrating',
            name='review',
            field=models.TextField(max_length=500, verbose_name='відгук'),
        ),
    ]
