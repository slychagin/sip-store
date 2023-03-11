# Generated by Django 4.1 on 2023-03-09 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_post_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='related_posts',
            field=models.ManyToManyField(blank=True, related_name='+', to='blog.post', verbose_name='схожі пости'),
        ),
        migrations.AddField(
            model_name='post',
            name='related_posts_title',
            field=models.CharField(blank='Схожі пости', max_length=255, verbose_name='заголовок до схожих постів'),
        ),
    ]