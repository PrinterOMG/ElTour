from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.misc import callbacks
from tgbot.services.database.models import Country, AuthorTour

account = InlineKeyboardMarkup(row_width=1)
account.add(
    InlineKeyboardButton('Изменить имя', callback_data=callbacks.account.new('update_name')),
    InlineKeyboardButton('Вкл/выкл рассылку', callback_data=callbacks.account.new('switch_mailing'))
)


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
