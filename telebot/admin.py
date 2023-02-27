from django.contrib import admin

from telebot.models import TelegramSettings


class TelegramSettingsAdmin(admin.ModelAdmin):
    list_display = ('tg_chat',)


admin.site.register(TelegramSettings, TelegramSettingsAdmin)
