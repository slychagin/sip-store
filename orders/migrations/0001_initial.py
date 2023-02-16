# Generated by Django 4.1 on 2023-02-15 07:11

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0004_remove_product_is_active_product_is_new_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=20, verbose_name='Номер замовлення')),
                ('customer_name', models.CharField(max_length=100, verbose_name='ПІБ')),
                ('phone', models.CharField(max_length=15, verbose_name='Телефон')),
                ('email', models.EmailField(max_length=50, verbose_name='E-mail')),
                ('city', models.CharField(max_length=50, verbose_name='Місто')),
                ('street', models.CharField(max_length=50, verbose_name='Вулиця')),
                ('house', models.CharField(max_length=10, verbose_name='Будинок')),
                ('room', models.CharField(max_length=10, verbose_name='Квартира')),
                ('new_post_city', models.CharField(max_length=50, verbose_name='Місто Нової Пошти')),
                ('new_post_office', models.CharField(max_length=100, verbose_name='Відділення Нової Пошти')),
                ('delivery_date', models.DateField(default=django.utils.timezone.localdate, verbose_name='Бажана дата доставки')),
                ('delivery_time', models.TimeField(verbose_name='Бажаний час доставки')),
                ('delivery_method', models.CharField(choices=[('COURIER', "Кур'єр по м. Золотоноша та м. Черкаси"), ('DELIVERY COMPANY', 'Доставка Новою Поштою')], default='COURIER', max_length=50, verbose_name='Спосіб доставки')),
                ('payment_method', models.CharField(choices=[('CASH', 'Готівка'), ('TERMINAL', "Кур'єру через термінал"), ('VISA', 'Оплата карткою VISA/MasterCard'), ('GOOGLE', 'Оплата Google Pay/Apple Pay')], default='CASH', max_length=50, verbose_name='Спосіб оплати')),
                ('communication_method', models.CharField(choices=[('PHONE', 'Телефон'), ('TELEGRAM', 'Telegram'), ('VIBER', 'Viber')], default='PHONE', max_length=20, verbose_name='Спосіб оплати')),
                ('order_note', models.CharField(blank=True, max_length=255, verbose_name='Примітка до замовлення')),
                ('order_total', models.IntegerField(verbose_name='Сума замовлення')),
                ('discount', models.IntegerField(verbose_name='Знижка')),
                ('ip', models.CharField(blank=True, max_length=20, verbose_name='IP адреса')),
                ('is_ordered', models.BooleanField(default=False, verbose_name='Замовлено')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')),
            ],
            options={
                'verbose_name': 'Замовлення',
                'verbose_name_plural': 'Замовлення',
                'ordering': ('-created',),
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(verbose_name='Ціна товару')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Кількість')),
                ('is_ordered', models.BooleanField(default=False, verbose_name='Замовлено')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order', verbose_name='Замовлення')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Товар в замовленні',
                'verbose_name_plural': 'Товари в замовленні',
                'ordering': ('-created',),
            },
        ),
    ]
