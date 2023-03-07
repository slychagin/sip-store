# Generated by Django 4.1 on 2023-03-03 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_productgallery_image_and_more'),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogcategory',
            options={'verbose_name': 'категорію', 'verbose_name_plural': 'категорії'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-created_date',), 'verbose_name': 'пост', 'verbose_name_plural': 'пости'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ('name',), 'verbose_name': 'тег', 'verbose_name_plural': 'теги'},
        ),
        migrations.AlterField(
            model_name='blogcategory',
            name='category_image',
            field=models.ImageField(blank=True, upload_to='photos/blog', verbose_name='фото категорії'),
        ),
        migrations.AlterField(
            model_name='blogcategory',
            name='category_name',
            field=models.CharField(max_length=100, unique=True, verbose_name='найменування категорії'),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='дата створення'),
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.TextField(blank=True, verbose_name='опис поста'),
        ),
        migrations.AlterField(
            model_name='post',
            name='is_available',
            field=models.BooleanField(default=True, verbose_name='доступний'),
        ),
        migrations.AlterField(
            model_name='post',
            name='mini_image',
            field=models.ImageField(upload_to='photos/blog/mini_images', verbose_name='міні фото до посту'),
        ),
        migrations.AlterField(
            model_name='post',
            name='modified_date',
            field=models.DateTimeField(auto_now=True, verbose_name='дата змін'),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='blog.blogcategory', verbose_name='категорія'),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_image',
            field=models.ImageField(blank=True, upload_to='photos/blog/images', verbose_name='фото до посту'),
        ),
        migrations.AlterField(
            model_name='post',
            name='quote',
            field=models.TextField(blank=True, verbose_name='цитата до посту'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=255, verbose_name='тема поста'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=100, verbose_name='назва тегу'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='store.product', verbose_name='продукт'),
        ),
    ]