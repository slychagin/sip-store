# Generated by Django 4.1 on 2023-02-27 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tg_token', models.CharField(max_length=100, verbose_name='Токен')),
                ('tg_chat', models.CharField(max_length=100, verbose_name='Чат ID')),
                ('tg_api', models.CharField(max_length=100, verbose_name='API адреса')),
                ('tg_message', models.TextField(blank=True, verbose_name='Текст повідомлення')),
                ('available', models.BooleanField(default=True, verbose_name='Активний')),
            ],
            options={
                'verbose_name_plural': 'Налаштування',
            },
        ),
    ]