import calendar
import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.misc import callbacks
from tgbot.services.database.models import Country, AuthorTour


account = InlineKeyboardMarkup(row_width=1)
account.add(
    InlineKeyboardButton('Изменить имя', callback_data=callbacks.account.new('update_name')),
    InlineKeyboardButton('Вкл/выкл рассылку', callback_data=callbacks.account.new('switch_mailing'))
)

cities = InlineKeyboardMarkup(row_width=1)
cities.add(
    InlineKeyboardButton('Новосибирск', callback_data=callbacks.city_pickup.new('Новосибирск')),
    InlineKeyboardButton('Санкт-Петербург', callback_data=callbacks.city_pickup.new('Санкт-Петербург')),
    InlineKeyboardButton('Москва', callback_data=callbacks.city_pickup.new('Москва'))
)

countries = InlineKeyboardMarkup(row_width=2)
countries.add(
    InlineKeyboardButton('Абхазия', callback_data=callbacks.country_pickup.new('Абхазия')),
    InlineKeyboardButton('Вьетнам', callback_data=callbacks.country_pickup.new('Вьетнам')),
    InlineKeyboardButton('Греция', callback_data=callbacks.country_pickup.new('Греция')),
    InlineKeyboardButton('Египет', callback_data=callbacks.country_pickup.new('Египет')),
    InlineKeyboardButton('Куба', callback_data=callbacks.country_pickup.new('Куба')),
    InlineKeyboardButton('Мальдивы', callback_data=callbacks.country_pickup.new('Мальдивы')),
    InlineKeyboardButton('ОАЭ', callback_data=callbacks.country_pickup.new('ОАЭ')),
    InlineKeyboardButton('Россия', callback_data=callbacks.country_pickup.new('Россия')),
    InlineKeyboardButton('Таиланд', callback_data=callbacks.country_pickup.new('Таиланд')),
    InlineKeyboardButton('Турция', callback_data=callbacks.country_pickup.new('Турция')),
    InlineKeyboardButton('Шри-Ланка', callback_data=callbacks.country_pickup.new('Шри-Ланка'))
)

adults_count = InlineKeyboardMarkup(row_width=4)
adults_count.add(
    InlineKeyboardButton('1', callback_data=callbacks.adults_count.new(1)),
    InlineKeyboardButton('2', callback_data=callbacks.adults_count.new(2)),
    InlineKeyboardButton('3', callback_data=callbacks.adults_count.new(3)),
    InlineKeyboardButton('4', callback_data=callbacks.adults_count.new(4)),
)

kids_count = InlineKeyboardMarkup(row_width=3)
kids_count.row(
    InlineKeyboardButton('Без детей', callback_data=callbacks.kids_count.new(0))
)
kids_count.row(
    InlineKeyboardButton('1', callback_data=callbacks.kids_count.new(1)),
    InlineKeyboardButton('2', callback_data=callbacks.kids_count.new(2)),
    InlineKeyboardButton('3', callback_data=callbacks.kids_count.new(3))
)

kid_age = InlineKeyboardMarkup(row_width=1)
kid_age.add(
    InlineKeyboardButton('0-1 год', callback_data=callbacks.kid_age.new('0-1')),
    InlineKeyboardButton('2-11 лет', callback_data=callbacks.kid_age.new('2-11')),
    InlineKeyboardButton('12+ лет', callback_data=callbacks.kid_age.new('12+'))
)

hotel_stars = InlineKeyboardMarkup(row_width=3)
hotel_stars.add(
    InlineKeyboardButton('⭐', callback_data=callbacks.hotel_stars.new(1)),
    InlineKeyboardButton('⭐⭐', callback_data=callbacks.hotel_stars.new(2)),
    InlineKeyboardButton('⭐⭐⭐', callback_data=callbacks.hotel_stars.new(3)),
    InlineKeyboardButton('⭐⭐⭐⭐', callback_data=callbacks.hotel_stars.new(4)),
    InlineKeyboardButton('⭐⭐⭐⭐⭐', callback_data=callbacks.hotel_stars.new(5))
)

food_type = InlineKeyboardMarkup(row_width=2)
food_type.add(
    InlineKeyboardButton('Любое', callback_data=callbacks.food_type.new('Любое')),
    InlineKeyboardButton('Всё включено', callback_data=callbacks.food_type.new('Всё включено')),
    InlineKeyboardButton('Завтрак', callback_data=callbacks.food_type.new('Завтрак')),
    InlineKeyboardButton('Полупансион', callback_data=callbacks.food_type.new('Полупансион')),
    InlineKeyboardButton('Полный пансион', callback_data=callbacks.food_type.new('Полный пансион'))
)

nights_count = InlineKeyboardMarkup(row_width=2)
nights_count.add(
    InlineKeyboardButton('5-7', callback_data=callbacks.nights_count.new('5-7')),
    InlineKeyboardButton('8-10', callback_data=callbacks.nights_count.new('8-10')),
    InlineKeyboardButton('11-13', callback_data=callbacks.nights_count.new('11-13')),
    InlineKeyboardButton('14+', callback_data=callbacks.nights_count.new('14+')),
)


def get_month_keyboard(year: int, month: int):
    months = {
        1: 'Январь',
        2: 'Февраль',
        3: 'Март',
        4: 'Апрель',
        5: 'Май',
        6: 'Июнь',
        7: 'Июль',
        8: 'Август',
        9: 'Сентябрь',
        10: 'Октябрь',
        11: 'Ноябрь',
        12: 'Декабрь'
    }

    first_day, days_in_month = calendar.monthrange(year, month)

    if days_in_month + first_day > 35:
        buttons_count = 42
    else:
        buttons_count = 35

    keyboard = InlineKeyboardMarkup(row_width=7)

    keyboard.row(
        InlineKeyboardButton(f'>>  {months[month]} {year}  <<', callback_data='pass')
    )

    keyboard.row(
        InlineKeyboardButton('Пн', callback_data='pass'),
        InlineKeyboardButton('Вт', callback_data='pass'),
        InlineKeyboardButton('Ср', callback_data='pass'),
        InlineKeyboardButton('Чт', callback_data='pass'),
        InlineKeyboardButton('Пт', callback_data='pass'),
        InlineKeyboardButton('Сб', callback_data='pass'),
        InlineKeyboardButton('Вс', callback_data='pass'),
    )

    buttons = list()
    day_of_month = datetime.datetime(year, month, 1)
    for i in range(buttons_count):
        if i < first_day or day_of_month.month != month:
            buttons.append(InlineKeyboardButton(' ', callback_data='pass'))
        else:
            buttons.append(
                InlineKeyboardButton(str(day_of_month.day), callback_data=callbacks.calendar.new(action='select', value=day_of_month.timestamp()))
            )
            day_of_month = day_of_month + datetime.timedelta(days=1)

    keyboard.add(*buttons)

    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year

    next_month = day_of_month.month
    next_year = day_of_month.year

    keyboard.add(
        InlineKeyboardButton(f'<<< {months[prev_month]} {prev_year}', callback_data=callbacks.calendar.new(action='show', value=f'{prev_year} {prev_month}')),
        InlineKeyboardButton(f'{months[next_month]} {next_year} >>>', callback_data=callbacks.calendar.new(action='show', value=f'{next_year} {next_month}'))
    )

    return keyboard


def get_countries_keyboard(countries: list[Country]):
    keyboard = InlineKeyboardMarkup(row_width=1)

    for country in countries:
        keyboard.add(
            InlineKeyboardButton(country.name, callback_data=callbacks.country.new(country.id))
        )

    return keyboard


def get_autor_tours_dates_keyboard(author_tours: list[AuthorTour]):
    keyboard = InlineKeyboardMarkup(row_width=1)

    for author_tour in author_tours:
        btn_text = f'{author_tour.pretty_month()} {author_tour.year}'
        keyboard.add(
            InlineKeyboardButton(btn_text, callback_data=callbacks.author_tour.new(action='show', id=author_tour.id))
        )

    keyboard.add(
        InlineKeyboardButton('Назад', callback_data='country_choose')
    )

    return keyboard


def get_author_tour_keyboard(author_tour: AuthorTour, landing_url: str):
    keyboard = InlineKeyboardMarkup(row_width=1)

    keyboard.add(
        InlineKeyboardButton('Узнать подробнее', url=landing_url),
        InlineKeyboardButton('Отправить заявку', callback_data=callbacks.author_tour.new(action='request', id=author_tour.id))
    )

    keyboard.add(
        InlineKeyboardButton('Назад', callback_data=callbacks.country.new(author_tour.country.id))
    )

    return keyboard
