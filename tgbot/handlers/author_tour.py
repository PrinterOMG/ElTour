from aiogram import Dispatcher
from aiogram.types import CallbackQuery, InputFile, MediaGroup
from aiogram.utils import markdown

from tgbot.config import Config
from tgbot.keyboards import inline_keyboards
from tgbot.misc import callbacks, messages
from tgbot.services.database.models import AuthorTour, Country, TelegramUser
from tgbot.services.utils import send_email


async def show_country_choose(call: CallbackQuery):
    db = call.bot.get('database')
    async with db() as session:
        countries = await Country.get_all(session)

    keyboard = inline_keyboards.get_countries_keyboard(countries)
    await call.message.edit_text(messages.author_tour_intro, reply_markup=keyboard)
    await call.answer()


async def show_author_tours_dates(call: CallbackQuery, callback_data: dict):
    country_id = callback_data['id']
    db = call.bot.get('database')
    async with db() as session:
        country = await session.get(Country, int(country_id))
        author_tours = await AuthorTour.get_by_country(session, country_id)

    keyboard = inline_keyboards.get_autor_tours_dates_keyboard(author_tours)

    await call.message.answer(messages.author_tour_choose.format(country=country.name), reply_markup=keyboard)
    await call.message.delete()
    await call.answer()


async def show_author_tour(call: CallbackQuery, callback_data: dict):
    tour_id = callback_data['id']
    db = call.bot.get('database')
    async with db.begin() as session:
        author_tour: AuthorTour = await session.get(AuthorTour, int(tour_id))

        text = messages.author_tour.format(
            country=author_tour.country.name,
            date=author_tour.pretty_date(),
            description=author_tour.description
        )
        keyboard = inline_keyboards.get_author_tour_keyboard(author_tour, author_tour.landing_url)

        if author_tour.image_url:
            photo = InputFile.from_url(author_tour.image_url)
            await call.message.answer_photo(photo, caption=text, reply_markup=keyboard)
            await call.message.delete()
        else:
            await call.message.edit_text(text, reply_markup=keyboard)

        await call.answer()


async def send_request(call: CallbackQuery, callback_data: dict):
    config: Config = call.bot.get('config')
    db = call.bot.get('database')
    async with db() as session:
        tg_user: TelegramUser = await session.get(TelegramUser, call.from_user.id)
        author_tour: AuthorTour = await session.get(AuthorTour, int(callback_data['id']))

    text = (
        'Описание заявки\n\n'
        f'Имя: {tg_user.name}\n'
        f'Телефон: {tg_user.phone}\n'
        f'Telegram: {tg_user.full_name} | {tg_user.mention or "(Нет обращения)"}\n\n'
        f'Страна: {author_tour.country.name}\n'
        f'Дата: {author_tour.pretty_date()}'
    )

    await send_email(
        subject=f'Заявка на авторский тур в {author_tour.country.name} от {tg_user.name}',
        body=text,
        sender=config.email.sender,
        receiver=config.email.reveiver,
        user=config.email.user,
        password=config.email.password
    )

    await call.message.answer(messages.author_tour_request_sent)
    await call.message.delete()
    await call.answer()


def register_author_tour(dp: Dispatcher):
    dp.register_callback_query_handler(show_country_choose, text='country_choose')
    dp.register_callback_query_handler(show_author_tours_dates, callbacks.country.filter())
    dp.register_callback_query_handler(show_author_tour, callbacks.author_tour.filter(action='show'))
    dp.register_callback_query_handler(send_request, callbacks.author_tour.filter(action='request'))
