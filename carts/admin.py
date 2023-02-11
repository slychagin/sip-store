from django.contrib import admin

from carts.forms import CouponAdminForm
from carts.models import Coupon


class CouponAdmin(admin.ModelAdmin):
    form = CouponAdminForm
    list_display = ('coupon_kod', 'discount', 'validity', 'is_available')
    search_fields = ('coupon_kod', 'discount', 'validity')
    list_per_page = 20
    list_max_show_all = 100
    list_editable = ('is_available',)


admin.site.register(Coupon, CouponAdmin)
