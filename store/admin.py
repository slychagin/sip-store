import admin_thumbnails
from django.contrib import admin
from django.utils.html import format_html
from embed_video.admin import AdminVideoMixin

from store.forms import (
    ProductAdminForm,
    ProductGalleryForm,
    ProductInfoAdminForm,
    ReviewRatingAdminForm,
)
from store.models import (
    Product,
    ProductGallery,
    ProductInfo,
    ReviewRating,
)


@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    form = ProductGalleryForm
    model = ProductGallery
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    prepopulated_fields = {'slug': ('product_name',)}
    list_display = (
        'product_name', 'price', 'category', 'modified_date',
        'is_available', 'is_new', 'is_sale', 'count_orders'
    )
    search_fields = ('product_name', 'category__category_name')
    list_per_page = 20
    list_max_show_all = 100
    list_editable = ('is_available', 'is_new', 'is_sale')
    inlines = [ProductGalleryInline]


class ProductGalleryAdmin(AdminVideoMixin, admin.ModelAdmin):
    form = ProductGalleryForm

    def thumbnail(self, obj):
        try:
            return format_html(f'<img src="{obj.image.url}" width="40"">')
        except ValueError:
            return format_html('<img>')

    thumbnail.short_description = 'Фото товару'
    list_display = ('product', 'thumbnail', 'video')
    list_display_links = ('product', 'thumbnail', 'video')
    list_filter = ('product',)
    search_fields = ('product__product_name',)
    list_per_page = 20
    list_max_show_all = 100


class ProductInfoAdmin(admin.ModelAdmin):
    form = ProductInfoAdminForm


class ReviewRatingAdmin(admin.ModelAdmin):
    form = ReviewRatingAdminForm
    list_display = ('product', 'rating', 'name', 'email', 'created_date', 'modified_date', 'is_moderated')
    list_display_links = ('product', 'rating', 'name')
    search_fields = ('product', 'rating', 'name', 'email', 'review', 'product__product_name')
    list_filter = ('is_moderated', 'product', 'rating', 'email', 'modified_date')
    list_editable = ('is_moderated',)
    list_per_page = 50
    list_max_show_all = 100


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductGallery, ProductGalleryAdmin)
admin.site.register(ProductInfo, ProductInfoAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)
