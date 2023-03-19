from django.contrib import admin

from contacts.models import SalePoint


class SalePointAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'street', 'house', 'schedule', 'mobile_phone', 'created', 'is_opened')
    search_fields = ('name', 'city', 'street')
    list_filter = ('city',)
    list_editable = ('is_opened',)
    list_per_page = 20
    list_max_show_all = 100


admin.site.register(SalePoint, SalePointAdmin)
