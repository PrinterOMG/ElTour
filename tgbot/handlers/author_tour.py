import datetime

from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InputFile, MediaGroup, Message, ContentType
from aiogram.utils import markdown

from tgbot.config import Config
from tgbot.keyboards import inline_keyboards, reply_keyboards
from tgbot.misc import callbacks, messages, states
from tgbot.misc.other import MONTHS
from tgbot.services.database.models import AuthorTour, Country, TelegramUser, AuthorTourRequest
from tgbot.services.uon import UonAPI
from tgbot.services.utils import send_email


async def show_country_choose(call: CallbackQuery):
    db = call.bot.get('database')
    async with db() as session:
        countries = await AuthorTour.get_countries(session)

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
    month = callback_data['month']

    db = call.bot.get('database')
    async with db.begin() as session:
        author_tour: AuthorTour = await session.get(AuthorTour, int(tour_id))

        text = messages.author_tour.format(
            country=author_tour.country.name,
            date=f'{month} {author_tour.year}',
            description=author_tour.description
        )
        keyboard = inline_keyboards.get_author_tour_keyboard(author_tour, month, author_tour.landing_url)

        if author_tour.image:
            photo = InputFile(author_tour.image)
            try:
                await call.message.answer_photo(photo, caption=text, reply_markup=keyboard)
                await call.message.delete()
            except:
                await call.message.edit_text(text, reply_markup=keyboard)
        else:
            await call.message.edit_text(text, reply_markup=keyboard)

        await call.answer()


async def get_phone(message: Message, state: FSMContext):
    contact = message.contact

    if contact.user_id != message.from_user.id:
        await message.answer(messages.not_your_phone)
        return

    phone = contact.phone_number.replace('+', '')

    bot = Bot.get_current()
    uon = bot.get('uon')
    db = bot.get('database')
    config = bot.get('config')
    user = await uon.get_user_by_phone(phone)
    async with db.begin() as session:
        tg_user = await session.get(TelegramUser, message.from_user.id)
        tg_user.phone = phone

        if user:
            birthday = user.get('u_birthday')
            tg_user.birthday = datetime.date.fromisoformat(birthday) if birthday else None
        else:
            uon: UonAPI = bot.get('uon')
            await uon.create_user(tg_user.name, phone)

    state_data = await state.get_data()
    await send_author_tour_email(tg_user, db, int(state_data['author_tour_id']), state_data['month'], config)
    await message.answer(messages.author_tour_request_sent, reply_markup=reply_keyboards.main_menu)
    await state.finish()


async def send_author_tour_email(tg_user: TelegramUser, db, author_tour_id: int, month, config: Config):
    async with db.begin() as session:
        author_tour: AuthorTour = await session.get(AuthorTour, author_tour_id)
        res = dict((v, k) for k, v in MONTHS.items())
        new_request = AuthorTourRequest(
            author_tour=author_tour,
            telegram_user=tg_user,
            created_at=datetime.datetime.now(),
            month=res[month]
        )
        session.add(new_request)

    text = (
        'Описание заявки\n\n'
        f'Имя: {tg_user.name}\n'
        f'Телефон: {tg_user.phone}\n'
        f'Telegram: {tg_user.full_name} | {tg_user.mention or "(Нет обращения)"}\n\n'
        f'Страна: {author_tour.country.name}\n'
        f'Дата: {month} {author_tour.year}'
    )

    await send_email(
        subject=f'Заявка на авторский тур в {author_tour.country.name} от {tg_user.name}',
        body=text,
        sender=config.email.sender,
        receiver=config.email.reveiver,
        user=config.email.user,
        password=config.email.password
    )


async def send_request(call: CallbackQuery, callback_data: dict, state: FSMContext):
    config: Config = call.bot.get('config')
    month = callback_data['month']
    db = call.bot.get('database')
    async with db() as session:
        tg_user: TelegramUser = await session.get(TelegramUser, call.from_user.id)
        if not tg_user.phone:
            await states.AuthorTour.waiting_for_phone.set()
            await call.message.answer(messages.phone_request, reply_markup=reply_keyboards.phone_request)
            await state.update_data(author_tour_id=callback_data['id'], month=month)
            await call.answer()
            return

    await send_author_tour_email(tg_user, db, int(callback_data['id']), month, config)

    await call.message.answer(messages.author_tour_request_sent)
    await call.message.delete()
    await call.answer()


def register_author_tour(dp: Dispatcher):
    dp.register_callback_query_handler(show_country_choose, text='country_choose')
    dp.register_callback_query_handler(show_author_tours_dates, callbacks.country.filter())
    dp.register_callback_query_handler(show_author_tour, callbacks.author_tour.filter(action='show'))
    dp.register_callback_query_handler(send_request, callbacks.author_tour.filter(action='request'))
    dp.register_message_handler(get_phone, state=states.AuthorTour.waiting_for_phone, content_types=[ContentType.CONTACT])
