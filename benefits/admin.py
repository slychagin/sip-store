from django.contrib import admin

from benefits.models import Benefits, Partners


class BenefitsAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


class PartnersAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(Benefits, BenefitsAdmin)
admin.site.register(Partners, PartnersAdmin)
