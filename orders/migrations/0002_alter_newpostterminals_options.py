# Generated by Django 4.1 on 2023-02-22 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newpostterminals',
            options={'ordering': ('city', 'terminal')},
        ),
    ]
