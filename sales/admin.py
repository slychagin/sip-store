from django.contrib import admin

from sales.models import (
    BestSellers,
    BlockTitle,
    MostPopularCenter,
    MostPopularLeft,
    MostPopularRight,
    NewProducts,
)


class BlockTitleAdmin(admin.ModelAdmin):
    list_display = ('title',)


class BestSellersAdmin(admin.ModelAdmin):
    list_display = ('title', 'product_1', 'product_2')


class NewProductsAdmin(admin.ModelAdmin):
    list_display = ('title', 'product_1', 'product_2')


class MostPopularLeftAdmin(admin.ModelAdmin):
    list_display = ('title', 'product_1', 'product_2', 'product_3')


class MostPopularCenterAdmin(admin.ModelAdmin):
    list_display = ('title', 'product_1', 'product_2', 'product_3')


class MostPopularRightAdmin(admin.ModelAdmin):
    list_display = ('title', 'product_1', 'product_2', 'product_3')


admin.site.register(BlockTitle, BlockTitleAdmin)
admin.site.register(BestSellers, BestSellersAdmin)
admin.site.register(NewProducts, NewProductsAdmin)
admin.site.register(MostPopularLeft, MostPopularLeftAdmin)
admin.site.register(MostPopularCenter, MostPopularCenterAdmin)
admin.site.register(MostPopularRight, MostPopularRightAdmin)
