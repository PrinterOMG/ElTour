from django.db import models
from multiselectfield import MultiSelectField


class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField(primary_key=True, verbose_name='Telegram ID')
    phone = models.CharField(max_length=16, null=True, verbose_name='Телефон')
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
    MONTHS_CHOICES = (
        ('jan', 'Январь'),
        ('feb', 'Февраль'),
        ('mar', 'Март'),
        ('apr', 'Апрель'),
        ('may', 'Май'),
        ('jun', 'Июнь'),
        ('jul', 'Июль'),
        ('aug', 'Август'),
        ('sep', 'Сентябрь'),
        ('oct', 'Октябрь'),
        ('nov', 'Ноябрь'),
        ('dec', 'Декабрь'),
    )

    country = models.ForeignKey('Country', on_delete=models.CASCADE, verbose_name='Страна')
    month = MultiSelectField(max_length=255, choices=MONTHS_CHOICES, verbose_name='Месяц')
    year = models.IntegerField(verbose_name='Год')
    description = models.TextField(verbose_name='Описание',
                                   help_text='Если нет картинки - лимит 4096 символов. Если есть картинка - лимит 1024 символа. Следите за лимитами!')
    landing_url = models.CharField(max_length=255, default='', blank=True, verbose_name='Ссылка на лендинг')
    image = models.ImageField(null=True, blank=True, upload_to='imgs/', verbose_name='Картинка')

    def months(self):
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
            'oct': 'Октябрь',
            'nov': 'Ноябрь',
            'dec': 'Декабрь'
        }

        return ', '.join(months[m] for m in self.month)

    months.short_description = 'Месяцы'

    class Meta:
        db_table = 'author_tour'
        verbose_name = 'Авторский тур'
        verbose_name_plural = 'Авторские туры'

    def __str__(self):
        return f'Тур - {self.country.name} | {self.months()} {self.year}'


class AuthorTourRequest(models.Model):
    MONTHS_CHOICES = (
        ('jan', 'Январь'),
        ('feb', 'Февраль'),
        ('mar', 'Март'),
        ('apr', 'Апрель'),
        ('may', 'Май'),
        ('jun', 'Июнь'),
        ('jul', 'Июль'),
        ('aug', 'Август'),
        ('sep', 'Сентябрь'),
        ('oct', 'Октябрь'),
        ('nov', 'Ноябрь'),
        ('dec', 'Декабрь'),
    )

    user = models.ForeignKey('TelegramUser', on_delete=models.CASCADE, verbose_name='Пользователь')
    author_tour = models.ForeignKey('AuthorTour', on_delete=models.CASCADE, verbose_name='Авторский тур')
    month = models.CharField(max_length=10, choices=MONTHS_CHOICES, verbose_name='Месяц')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заявки')


    def __str__(self):
        return f'Заявка на {self.author_tour}'

    class Meta:
        db_table = 'author_tour_request'
        verbose_name = 'Заявка на авторский тур'
        verbose_name_plural = 'Заявки на авторские тур'


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
