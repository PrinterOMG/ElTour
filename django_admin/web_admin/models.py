from django.db import models


class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField(primary_key=True, verbose_name='Telegram ID')
    phone = models.CharField(max_length=16, verbose_name='Телефон')
    name = models.CharField(max_length=32, verbose_name='Имя')
    full_name = models.CharField(max_length=128, default='', verbose_name='Имя в Telegram')
    mention = models.CharField(max_length=128, default='', verbose_name='Обращение в Telegram')
    mailing_sub = models.BooleanField(default=True, verbose_name='Подписка на рассылку')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    class Meta:
        db_table = 'telegram_user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.mention or self.full_name or self.phone
