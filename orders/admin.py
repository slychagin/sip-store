from django.contrib import admin

from orders.models import Order, OrderItem, Customers, Subscribers


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'quantity', 'price', 'is_ordered')
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'phone', 'email', 'order_total')
    search_fields = ('order_number', 'customer_name', 'phone', 'email', 'order_total')
    list_per_page = 50
    list_max_show_all = 100
    inlines = [OrderItemInline]


class CustomersAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'phone', 'email', 'note')
    search_fields = ('customer_name', 'phone', 'email')
    list_per_page = 50
    list_max_show_all = 100


class SubscribersAdmin(admin.ModelAdmin):
    list_display = ('email',)
    search_fields = ('email',)
    list_per_page = 50
    list_max_show_all = 100


admin.site.register(Order, OrderAdmin)
admin.site.register(Customers, CustomersAdmin)
admin.site.register(Subscribers, SubscribersAdmin)
admin.site.register(OrderItem)
