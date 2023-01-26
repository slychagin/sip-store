from django.contrib import admin

from sales.models import (
    BlockTitle,
    BestSellers,
    NewProducts
)


class BlockTitleAdmin(admin.ModelAdmin):
    list_display = ('title',)


class BestSellersAdmin(admin.ModelAdmin):
    list_display = ('title', 'product_1', 'product_2')


class NewProductsAdmin(admin.ModelAdmin):
    list_display = ('title', 'product_1', 'product_2')


admin.site.register(BlockTitle, BlockTitleAdmin)
admin.site.register(BestSellers, BestSellersAdmin)
admin.site.register(NewProducts, NewProductsAdmin)
