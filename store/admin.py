from django.contrib import admin
from store.models import Product


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}
    list_display = ('product_name', 'price', 'category', 'modified_date', 'is_available')
    search_fields = ('product_name', 'category__category_name')
    list_per_page = 20
    list_max_show_all = 100


admin.site.register(Product, ProductAdmin)
