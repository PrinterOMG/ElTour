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


class Country(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название')

    class Meta:
        db_table = 'country'
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


class AuthorTour(models.Model):
    MONTHS = (
        ('jan', 'Январь'),
        ('feb', 'Февраль'),
        ('mar', 'Март'),
        ('apr', 'Апрель'),
        ('may', 'Май'),
        ('jun', 'Июнь'),
        ('jul', 'Июль'),
        ('aug', 'Август'),
        ('sep', 'Сентябрь'),
        ('nov', 'Ноябрь'),
        ('dec', 'Декабрь'),
    )

    country = models.ForeignKey('Country', on_delete=models.CASCADE, verbose_name='Страна')
    month = models.CharField(max_length=3, choices=MONTHS, verbose_name='Месяц')
    year = models.IntegerField(verbose_name='Год')
    description = models.TextField(verbose_name='Описание')
    landing_url = models.CharField(max_length=255, default='', blank=True, verbose_name='Ссылка на лендинг')
    image_url = models.CharField(max_length=255, default='', blank=True, verbose_name='Ссылка на картинку')
    image_tg_id = models.CharField(max_length=255, default='', blank=True)

    class Meta:
        db_table = 'author_tour'
        verbose_name = 'Авторский тур'
        verbose_name_plural = 'Авторские туры'
