from django.db import models


class TelegramSettings(models.Model):
    objects = models.Manager()

    tg_token = models.CharField(max_length=100, verbose_name='Токен')
    tg_chat = models.CharField(max_length=100, verbose_name='Чат ID')
    tg_api = models.CharField(max_length=100, verbose_name='API адреса')
    tg_message = models.TextField(blank=True, verbose_name='Текст повідомлення')
    available = models.BooleanField(default=True, verbose_name='Активний')

    def __str__(self):
        return self.tg_chat

    class Meta:
        verbose_name_plural = 'Налаштування'
