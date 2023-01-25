from django.contrib import admin

from category.models import Category


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')
    search_fields = ('category_name',)
    list_per_page = 20


admin.site.register(Category, CategoryAdmin)
