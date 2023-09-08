import datetime

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, Message

from tgbot.config import Config
from tgbot.handlers.main_menu import start_tour_pickup
from tgbot.handlers.other import cancel
from tgbot.keyboards import inline_keyboards, reply_keyboards
from tgbot.misc import states, messages, callbacks, reply_commands
from tgbot.services.database.models import TourPickup, TelegramUser
from tgbot.services.uon import UonAPI
from tgbot.services.utils import send_email


async def get_city(call: CallbackQuery, callback_data: dict, state: FSMContext):
    city = callback_data['name']
    await state.update_data(city=city)

    state_data = await state.get_data()
    if state_data.get('update'):
        await show_confirm(call, state)
        return

    await states.TourPickup.next()

    await call.message.edit_text(messages.tour_country_input.format(departure_city=city), reply_markup=inline_keyboards.countries)
    await call.answer()


async def get_city_input(message: Message, state: FSMContext):
    city = message.text
    await state.update_data(city=city)

    state_data = await state.get_data()
    if state_data.get('update'):
        await show_confirm(message, state)
        return

    await states.TourPickup.next()

    await message.answer(messages.tour_country_input.format(departure_city=city), reply_markup=inline_keyboards.countries)


async def get_country(call: CallbackQuery, callback_data: dict, state: FSMContext):
    country = callback_data['name']
    await state.update_data(country=country)

    state_data = await state.get_data()
    if state_data.get('update'):
        await show_confirm(call, state)
        return

    await states.TourPickup.next()

    await call.message.edit_text(messages.adults_count_input.format(tour_country=country), reply_markup=inline_keyboards.adults_count)
    await call.answer()


async def get_country_input(message: Message, state: FSMContext):
    country = message.text
    await state.update_data(country=country)

    state_data = await state.get_data()
    if state_data.get('update'):
        await show_confirm(message, state)
        return

    await states.TourPickup.next()

    await message.answer(messages.adults_count_input.format(tour_country=country), reply_markup=inline_keyboards.adults_count)


async def get_adults_count(call: CallbackQuery, callback_data: dict, state: FSMContext):
    count = callback_data['count']
    await state.update_data(adults_count=count)

    state_data = await state.get_data()
    if state_data.get('update'):
        await show_confirm(call, state)
        return

    await states.TourPickup.next()

    await call.message.edit_text(messages.kids_count_input.format(adults_count=count), reply_markup=inline_keyboards.kids_count)
    await call.answer()


async def get_adults_count_input(message: Message, state: FSMContext):
    count = message.text

    if not count.isdigit():
        await message.answer(messages.bad_adults_count)
        return

    await state.update_data(adults_count=count)

    state_data = await state.get_data()
    if state_data.get('update'):
        await show_confirm(message, state)
        return

    await states.TourPickup.next()

    await message.answer(messages.kids_count_input.format(adults_count=count), reply_markup=inline_keyboards.kids_count)


async def get_kids_count(call: CallbackQuery, callback_data: dict, state: FSMContext):
    count = callback_data['count']
    await state.update_data(kids_count=count)

    if int(count) == 0:
        state_data = await state.get_data()
        if state_data.get('update'):
            await show_confirm(call, state)
            return

        await call.message.edit_text(messages.hotel_stars_input.format(kids_count=count), reply_markup=inline_keyboards.hotel_stars)
        await states.TourPickup.waiting_for_hotel_stars.set()
    else:
        await call.message.edit_text(messages.kids_age_input.format(kids_count=count, kid_num='1'), reply_markup=inline_keyboards.kid_age)
        await states.TourPickup.next()

    await call.answer()


async def get_kids_count_input(message: Message, state: FSMContext):
    count = message.text

    if not count.isdigit():
        await message.answer(messages.bad_kids_count)
        return

    await state.update_data(kids_count=count)

    if int(count) == 0:
        state_data = await state.get_data()
        if state_data.get('update'):
            await show_confirm(message, state)
            return

        await message.answer(messages.hotel_stars_input.format(kids_count=count), reply_markup=inline_keyboards.hotel_stars)
        await states.TourPickup.waiting_for_hotel_stars.set()
    else:
        await message.answer(messages.kids_age_input.format(kids_count=count, kid_num=1), reply_markup=inline_keyboards.kid_age)
        await states.TourPickup.next()


async def get_kid_age(call: CallbackQuery, callback_data: dict, state: FSMContext):
    kid_age = callback_data['age']

    async with state.proxy() as data:
        kid_ages = data.get('kid_ages', default=[])
        kid_ages.append(kid_age)
        data['kid_ages'] = kid_ages

        kid_num = int(data.get('kid_num', default=1))
        data['kid_num'] = kid_num + 1

    kids_count = int(data['kids_count'])
    if kid_num == kids_count:
        state_data = await state.get_data()
        if state_data.get('update'):
            await show_confirm(call, state)
            return

        await call.message.edit_text(messages.hotel_stars_input.format(kids_count=kids_count), reply_markup=inline_keyboards.hotel_stars)
        await states.TourPickup.next()
    else:
        await call.message.edit_text(messages.kids_age_input.format(kids_count=kids_count, kid_num=kid_num+1), reply_markup=inline_keyboards.kid_age)

    await call.answer()


async def get_hotel_stars(call: CallbackQuery, callback_data: dict, state: FSMContext):
    stars = int(callback_data['stars'])
    await state.update_data(hotel_stars=stars)

    state_data = await state.get_data()
    if state_data.get('update'):
        await show_confirm(call, state)
        return

    await states.TourPickup.next()

    await call.message.edit_text(messages.food_type_input.format(hotel_stars='⭐' * stars), reply_markup=inline_keyboards.food_type)
    await call.answer()


async def get_food_type(call: CallbackQuery, callback_data: dict, state: FSMContext):
    food_type = callback_data['type']
    await state.update_data(food_type=food_type)

    state_data = await state.get_data()
    if state_data.get('update'):
        await show_confirm(call, state)
        return

    await states.TourPickup.next()

    cur_date = datetime.date.today()
    await call.message.edit_text(messages.date_input.format(food_type=food_type),
                                 reply_markup=inline_keyboards.get_month_keyboard(cur_date.year, cur_date.month))
    await call.answer()


async def get_date(call: CallbackQuery, callback_data: dict, state: FSMContext):
    date = callback_data['value']
    selected_date = datetime.date.fromtimestamp(float(date))
    cur_date = datetime.date.today()

    if selected_date < cur_date:
        await call.answer(messages.old_date, show_alert=True)
        return

    await state.update_data(date=date)

    state_data = await state.get_data()
    if state_data.get('update'):
        await show_confirm(call, state)
        return

    await states.TourPickup.next()

    await call.message.edit_text(messages.nights_count_input.format(date=selected_date.isoformat()),
                                 reply_markup=inline_keyboards.nights_count)
    await call.answer()


async def show_month(call: CallbackQuery, callback_data: dict):
    year, month = map(int, callback_data['value'].split())
    await call.message.edit_reply_markup(inline_keyboards.get_month_keyboard(year, month))
    await call.answer()


async def get_nights_count(call: CallbackQuery, callback_data: dict, state: FSMContext):
    count = callback_data['count']
    await state.update_data(nights_count=count)

    await show_confirm(call, state)


def get_tour_pickup_message(state_data):
    kids_age_str = ''
    kids_count = int(state_data['kids_count'])
    if kids_count != 0:
        kids_age = state_data['kid_ages']
        for kid_num in range(1, kids_count + 1):
            kids_age_str += f'\t- Возраст {kid_num}-го ребенка: {kids_age[kid_num - 1]}\n'
        kids_age_str += '\n'

    date = datetime.date.fromtimestamp(float(state_data['date']))
    text = messages.tour_pickup_confirmation.format(
        country=state_data['country'],
        adults_count=state_data['adults_count'],
        kids_count=kids_count,
        kids_age=kids_age_str,
        hotel_stars=int(state_data['hotel_stars']) * '⭐',
        food_type=state_data['food_type'],
        nights_count=state_data['nights_count'],
        city=state_data['city'],
        date=date.isoformat()
    )

    return text


async def show_confirm(event: CallbackQuery | Message, state: FSMContext):
    await states.TourPickup.finishing.set()

    state_data = await state.get_data()
    text = get_tour_pickup_message(state_data)

    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text, reply_markup=inline_keyboards.tour_pickup_confirm)
        await event.answer()
    else:
        await event.answer(text, reply_markup=inline_keyboards.tour_pickup_confirm)


async def show_edit_keyboard(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    kids_count = int(state_data['kids_count'])

    await call.message.edit_reply_markup(inline_keyboards.get_edit_keyboard(kids_count != 0))
    await call.answer()


async def show_confirm_keyboard(call: CallbackQuery):
    await call.message.edit_reply_markup(inline_keyboards.tour_pickup_confirm)
    await call.answer()


async def start_over(message: Message, state: FSMContext):
    await state.reset_data()
    await start_tour_pickup(message)


async def back(message: Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state not in (states.TourPickup.waiting_for_city, states.TourPickup.waiting_for_hotel_stars):
        await states.TourPickup.previous()

    state_data = await state.get_data()
    match current_state:
        case states.TourPickup.waiting_for_city.state:
            await cancel(message, state)

        case states.TourPickup.waiting_for_country.state:
            await message.answer(messages.departure_city_input, reply_markup=inline_keyboards.cities)

        case states.TourPickup.waiting_for_adult_count.state:
            await message.answer(messages.tour_country_input.format(departure_city=state_data['city']),
                                 reply_markup=inline_keyboards.countries)

        case states.TourPickup.waiting_for_kids_count.state:
            await message.answer(messages.adults_count_input.format(tour_country=state_data['country']),
                                 reply_markup=inline_keyboards.adults_count)

        case states.TourPickup.waiting_for_kids_age.state:
            await state.update_data(kid_num=1, kid_ages=[])
            await message.answer(messages.kids_count_input.format(adults_count=state_data['adults_count']),
                                 reply_markup=inline_keyboards.kids_count)

        case states.TourPickup.waiting_for_hotel_stars.state:
            kids_count = int(state_data['kids_count'])
            if kids_count == 0:
                await states.TourPickup.waiting_for_kids_count.set()
                await message.answer(messages.kids_count_input.format(adults_count=state_data['adults_count']),
                                     reply_markup=inline_keyboards.kids_count)
            else:
                await states.TourPickup.waiting_for_kids_age.set()
                await state.update_data(kid_num=1, kid_ages=[])
                await message.answer(messages.kids_age_input.format(kids_count=kids_count, kid_num=1),
                                     reply_markup=inline_keyboards.kid_age)

        case states.TourPickup.waiting_for_food_type.state:
            await message.answer(messages.hotel_stars_input.format(kids_count=state_data['kids_count']),
                                 reply_markup=inline_keyboards.hotel_stars)

        case states.TourPickup.waiting_for_date.state:
            await message.answer(messages.food_type_input.format(hotel_stars='⭐' * int(state_data['stars'])),
                                 reply_markup=inline_keyboards.food_type)

        case states.TourPickup.waiting_for_nights_count.state:
            cur_date = datetime.date.today()
            await message.answer(messages.date_input.format(food_type=state_data['food_type']),
                                 reply_markup=inline_keyboards.get_month_keyboard(cur_date.year, cur_date.month))

        case states.TourPickup.finishing.state:
            date = datetime.date.fromtimestamp(float(state_data['date']))
            await message.answer(messages.nights_count_input.format(date=date.isoformat()),
                                 reply_markup=inline_keyboards.nights_count)


async def update_data(call: CallbackQuery, callback_data: dict, state: FSMContext):
    update_value = callback_data['payload']

    await state.update_data(update=1)
    state_data = await state.get_data()

    match update_value:
        case 'city':
            await call.message.edit_text(messages.departure_city_input, reply_markup=inline_keyboards.cities)
            await states.TourPickup.waiting_for_city.set()

        case 'country':
            await call.message.edit_text(messages.tour_country_input.format(departure_city=state_data['city']),
                                         reply_markup=inline_keyboards.countries)
            await states.TourPickup.waiting_for_country.set()

        case 'adults_count':
            await call.message.edit_text(messages.adults_count_input.format(tour_country=state_data['country']),
                                         reply_markup=inline_keyboards.adults_count)
            await states.TourPickup.waiting_for_adult_count.set()

        case 'kids_count':
            await state.update_data(kid_num=1, kid_ages=[])
            await call.message.edit_text(messages.kids_count_input.format(adults_count=state_data['adults_count']),
                                         reply_markup=inline_keyboards.kids_count)
            await states.TourPickup.waiting_for_kids_count.set()

        case 'kids_age':
            await state.update_data(kid_num=1, kid_ages=[])
            await call.message.edit_text(messages.kids_age_input.format(kids_count=state_data['kids_count'], kid_num=1),
                                         reply_markup=inline_keyboards.kid_age)
            await states.TourPickup.waiting_for_kids_age.set()

        case 'hotel_stars':
            await call.message.edit_text(messages.hotel_stars_input.format(kids_count=state_data['kids_count']),
                                         reply_markup=inline_keyboards.hotel_stars)
            await states.TourPickup.waiting_for_hotel_stars.set()

        case 'food_type':
            await call.message.edit_text(messages.hotel_stars_input.format(kids_count=state_data['kids_count']),
                                         reply_markup=inline_keyboards.hotel_stars)
            await states.TourPickup.waiting_for_food_type.set()

        case 'date':
            cur_date = datetime.date.today()
            await call.message.edit_text(messages.date_input.format(food_type=state_data['food_type']),
                                         reply_markup=inline_keyboards.get_month_keyboard(cur_date.year, cur_date.month))
            await states.TourPickup.waiting_for_date.set()

        case 'nights_count':
            date = datetime.date.fromtimestamp(float(state_data['date']))
            await call.message.edit_text(messages.nights_count_input.format(date=date.isoformat()),
                                         reply_markup=inline_keyboards.nights_count)
            await states.TourPickup.waiting_for_nights_count.set()

    await call.answer()


async def confirm_tour_pickup(call: CallbackQuery, state: FSMContext):
    db = call.bot.get('database')

    state_data = await state.get_data()
    async with db.begin() as session:
        tg_user = await session.get(TelegramUser, call.from_user.id)
        new_tour_pickup = TourPickup(
            departure_city=state_data['city'],
            country=state_data['country'],
            adults_count=int(state_data['adults_count']),
            kids_count=int(state_data['kids_count']),
            kids_ages=';'.join(state_data.get('kid_ages', [])),
            hotel_stars=int(state_data['hotel_stars']),
            food_type=state_data['food_type'],
            date=datetime.date.fromtimestamp(float(state_data['date'])),
            night_count=state_data['nights_count'],
            telegram_user_id=call.from_user.id
        )
        session.add(new_tour_pickup)

    config: Config = call.bot.get('config')
    text = get_tour_pickup_message(state_data)

    text += (
        f'\n\nИмя: {tg_user.name}\n'
        f'Телефон: {tg_user.phone}\n'
        f'Telegram: {tg_user.full_name} | {tg_user.mention or "(Нет обращения)"}'
    )

    await send_email(
        subject=f'Заявка на подбор тура от {tg_user.name}',
        body=text,
        sender=config.email.sender,
        receiver=config.email.reveiver,
        user=config.email.user,
        password=config.email.password
    )

    await call.answer()
    await state.finish()

    if not tg_user.birthday:
        await call.message.answer(messages.tour_pickup_complete)
        await states.Birthday.first()
        await call.message.answer(messages.birthday_input, reply_markup=reply_keyboards.cancel)
    else:
        await call.message.answer(messages.tour_pickup_complete, reply_markup=reply_keyboards.main_menu)


def register_tour_pickup(dp: Dispatcher):
    dp.register_message_handler(back, Text(equals=reply_commands.back), state='*')
    dp.register_message_handler(start_over, Text(equals=reply_commands.start_over), state='*')

    dp.register_callback_query_handler(get_city, callbacks.city_pickup.filter(), state=states.TourPickup.waiting_for_city)
    dp.register_message_handler(get_city_input, state=states.TourPickup.waiting_for_city)

    dp.register_callback_query_handler(get_country, callbacks.country_pickup.filter(), state=states.TourPickup.waiting_for_country)
    dp.register_message_handler(get_country_input, state=states.TourPickup.waiting_for_country)

    dp.register_callback_query_handler(get_adults_count, callbacks.adults_count.filter(), state=states.TourPickup.waiting_for_adult_count)
    dp.register_message_handler(get_adults_count_input, state=states.TourPickup.waiting_for_adult_count)

    dp.register_callback_query_handler(get_kids_count, callbacks.kids_count.filter(), state=states.TourPickup.waiting_for_kids_count)
    dp.register_message_handler(get_kids_count_input, state=states.TourPickup.waiting_for_kids_count)

    dp.register_callback_query_handler(get_kid_age, callbacks.kid_age.filter(), state=states.TourPickup.waiting_for_kids_age)

    dp.register_callback_query_handler(get_hotel_stars, callbacks.hotel_stars.filter(), state=states.TourPickup.waiting_for_hotel_stars)

    dp.register_callback_query_handler(get_food_type, callbacks.food_type.filter(), state=states.TourPickup.waiting_for_food_type)

    dp.register_callback_query_handler(get_date, callbacks.calendar.filter(action='select'), state=states.TourPickup.waiting_for_date)
    dp.register_callback_query_handler(show_month, callbacks.calendar.filter(action='show'), state=states.TourPickup.waiting_for_date)

    dp.register_callback_query_handler(get_nights_count, callbacks.nights_count.filter(), state=states.TourPickup.waiting_for_nights_count)

    dp.register_callback_query_handler(show_confirm_keyboard, callbacks.tour_pickup.filter(action='back'),state=states.TourPickup.finishing)
    dp.register_callback_query_handler(show_edit_keyboard, callbacks.tour_pickup.filter(action='edit'), state=states.TourPickup.finishing)
    dp.register_callback_query_handler(confirm_tour_pickup, callbacks.tour_pickup.filter(action='confirm'), state=states.TourPickup.finishing)
    dp.register_callback_query_handler(update_data, callbacks.tour_pickup.filter(action='update'), state=states.TourPickup.finishing)
