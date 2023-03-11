# Generated by Django 4.1 on 2023-03-10 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_delete_postcomment'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name="ім'я")),
                ('email', models.EmailField(max_length=100, verbose_name='E-mail')),
                ('content', models.TextField(verbose_name='коментар')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='дата створення')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='дата коригування')),
                ('is_moderated', models.BooleanField(default=False, verbose_name='промодерований')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.post', verbose_name='пост')),
            ],
            options={
                'verbose_name': 'коментар',
                'verbose_name_plural': 'коментари',
                'ordering': ('-created_date',),
            },
        ),
    ]