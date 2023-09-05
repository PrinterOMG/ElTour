from django.db import models


class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField(primary_key=True, verbose_name='Telegram ID')
    phone = models.CharField(max_length=16, verbose_name='Телефон')
    name = models.CharField(max_length=32, verbose_name='Имя')
    birthday = models.DateField(null=True, verbose_name='День рождения')
    full_name = models.CharField(max_length=128, default='', verbose_name='Имя в Telegram')
    mention = models.CharField(max_length=128, default='', verbose_name='Обращение в Telegram')
    mailing_sub = models.BooleanField(default=True, verbose_name='Подписка на рассылку')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    salebot_id = models.BigIntegerField(null=True)

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

    def __str__(self):
        return self.name


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

    def __str__(self):
        months = {
            'jan': 'Январь',
            'feb': 'Февраль',
            'mar': 'Март',
            'apr': 'Апрель',
            'may': 'Май',
            'jun': 'Июнь',
            'jul': 'Июль',
            'aug': 'Август',
            'sep': 'Сентябрь',
            'nov': 'Ноябрь',
            'dec': 'Декабрь'
        }

        return f'Тур - {self.country.name} | {months[self.month]} {self.year}'


class TourPickup(models.Model):
    departure_city = models.CharField(max_length=64, verbose_name='Город вылета')
    country = models.CharField(max_length=64, verbose_name='Страна для путешествия')
    adults_count = models.IntegerField(verbose_name='Кол-во взрослых')
    kids_count = models.IntegerField(verbose_name='Кол-во детей')
    kids_ages = models.CharField(max_length=255)
    hotel_stars = models.IntegerField(verbose_name='Категория отеля')
    food_type = models.CharField(max_length=32, verbose_name='Тип питания')
    date = models.DateField(verbose_name='Дата вылета')
    night_count = models.CharField(max_length=16, verbose_name='Кол-во ночей')

    telegram_user = models.ForeignKey('TelegramUser', on_delete=models.CASCADE, verbose_name='Пользователь')

    def pretty_kids_ages(self):
        if self.kids_ages:
            kids_ages = self.kids_ages.split(';')
            return '\n'.join(f'- Возраст {kid_num}-го ребенка: {age}' for kid_num, age in enumerate(kids_ages, start=1))

        return ''

    def pretty_stars(self):
        return self.hotel_stars * '⭐'

    pretty_kids_ages.short_description = 'Возраст детей'
    pretty_stars.short_description = 'Категория отеля'

    class Meta:
        db_table = 'tour_pickup'
        verbose_name = 'Заявка на тур'
        verbose_name_plural = 'Заявки на тур'
