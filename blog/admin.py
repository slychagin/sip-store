from django.contrib import admin

from blog.forms import PostAdminForm
from blog.models import BlogCategory, Post, Tag


class BlogCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')
    search_fields = ('category_name',)
    list_per_page = 20


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'post_category', 'created_date', 'is_available')
    search_fields = ('title', 'post_category')
    list_per_page = 20
    list_max_show_all = 100
    list_editable = ('is_available',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'product')


admin.site.register(BlogCategory, BlogCategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
