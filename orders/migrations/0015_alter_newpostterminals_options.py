# Generated by Django 4.1 on 2023-02-21 11:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_newpostterminals'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newpostterminals',
            options={'ordering': ('city',)},
        ),
    ]
