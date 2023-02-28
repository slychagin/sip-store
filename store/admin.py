from django.contrib import admin

from store.models import Product


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}
    list_display = (
        'product_name', 'price', 'category', 'modified_date',
        'is_available', 'is_new', 'is_sale', 'count_orders'
    )
    search_fields = ('product_name', 'category__category_name')
    list_per_page = 20
    list_max_show_all = 100
    list_editable = ('is_available', 'is_new', 'is_sale')


admin.site.register(Product, ProductAdmin)
