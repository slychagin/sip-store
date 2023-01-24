from django.contrib import admin
from benefits.models import Benefits


class BenefitsAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


admin.site.register(Benefits, BenefitsAdmin)
