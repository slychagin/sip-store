from django.contrib import admin

from blog.forms import PostAdminForm
from blog.models import BlogCategory, Post, Tag, PostComment


class BlogCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')
    search_fields = ('category_name',)
    list_per_page = 20


class PostCommentInline(admin.TabularInline):
    model = PostComment
    extra = 0


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'post_category', 'created_date', 'is_available')
    search_fields = ('title', 'post_category')
    list_per_page = 20
    list_max_show_all = 100
    list_editable = ('is_available',)
    inlines = [PostCommentInline]


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'product')


class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'name', 'email', 'content', 'created_date', 'modified_date', 'is_moderated')
    list_display_links = ('post', 'name', 'email')
    search_fields = ('name', 'email', 'content', 'post__title')
    list_filter = ('is_moderated', 'post', 'email', 'modified_date')
    list_editable = ('is_moderated',)
    list_per_page = 20
    list_max_show_all = 100


admin.site.register(BlogCategory, BlogCategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(PostComment, PostCommentAdmin)
