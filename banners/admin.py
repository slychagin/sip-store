from django.contrib import admin

from banners.models import WeekOfferBanner


class WeekOfferBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'product')


admin.site.register(WeekOfferBanner, WeekOfferBannerAdmin)
