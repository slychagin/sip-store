from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from banners.models import (
    WeekOfferBanner,
    MainBanner,
    TwoBanners,
    OfferSingleBanner,
    FooterBanner, BackgroundBanner
)


class WeekOfferBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'product', 'countdown')


class MainBannerAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        return format_html(f'<img src="{obj.image.url}" width="100"">')

    thumbnail.short_description = _('фото')
    list_display = ('title', 'banner_url', 'thumbnail')


class TwoBannersAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        return format_html(f'<img src="{obj.image.url}" width="100"">')

    thumbnail.short_description = _('фото')
    list_display = ('title', 'banner_url', 'thumbnail')


class OfferSingleBannerAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        return format_html(f'<img src="{obj.image.url}" width="100"">')

    thumbnail.short_description = _('фото')
    list_display = ('thumbnail', 'banner_url')


class FooterBannerAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        return format_html(f'<img src="{obj.image.url}" width="100"">')

    thumbnail.short_description = _('фото')
    list_display = ('thumbnail', 'banner_url')


class BackgroundBannerAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        return format_html(f'<img src="{obj.image.url}" width="120" height="20"">')

    thumbnail.short_description = _('фото')
    list_display = ('thumbnail', 'banner_url')


admin.site.register(WeekOfferBanner, WeekOfferBannerAdmin)
admin.site.register(MainBanner, MainBannerAdmin)
admin.site.register(TwoBanners, TwoBannersAdmin)
admin.site.register(OfferSingleBanner, OfferSingleBannerAdmin)
admin.site.register(FooterBanner, FooterBannerAdmin)
admin.site.register(BackgroundBanner, BackgroundBannerAdmin)
