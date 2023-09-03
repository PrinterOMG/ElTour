import datetime

from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType, ReplyKeyboardRemove

from tgbot.keyboards import reply_keyboards
from tgbot.misc import states, messages
from tgbot.services.database.models import TelegramUser
from tgbot.services.uon import UonAPI


async def get_phone(message: Message, state: FSMContext):
    contact = message.contact

    if message.from_id != contact.user_id:
        await message.answer(messages.not_your_phone, reply_markup=reply_keyboards.phone_request)
        return

    phone = contact.phone_number.replace('+', '')

    bot = Bot.get_current()
    uon = bot.get('uon')
    user = await uon.get_user_by_phone(phone)
    if user:
        db = bot.get('database')
        birthday = user.get('u_birthday')
        async with db.begin() as session:
            new_user = TelegramUser(
                telegram_id=message.from_id,
                name=user.get('u_name', ''),
                full_name=message.from_user.full_name,
                mention=message.from_user.mention,
                phone=phone,
                birthday=datetime.date.fromisoformat(birthday) if birthday else None
            )
            session.add(new_user)
        return

    await state.update_data(phone=phone)
    await message.answer(messages.name_input, reply_markup=ReplyKeyboardRemove())
    await states.Registration.next()


async def get_name(message: Message, state: FSMContext):
    name = message.text

    if len(name) > 32:
        await message.answer(messages.long_name)
        return

    await state.update_data(name=name)
    await message.answer(messages.birthday_input)
    await states.Registration.next()


async def get_birthday(message: Message, state: FSMContext):
    birthday = message.text

    try:
        birthday = datetime.datetime.strptime(birthday, '%d.%m.%Y').date()
    except ValueError:
        await message.answer(messages.bad_birthday)

    bot = Bot.get_current()

    db = bot.get('database')
    state_data = await state.get_data()
    async with db.begin() as session:
        new_user = TelegramUser(
            telegram_id=message.from_id,
            name=state_data['name'],
            full_name=message.from_user.full_name,
            mention=message.from_user.mention,
            phone=state_data['phone'],
            birthday=birthday.isoformat()
        )
        session.add(new_user)

    uon: UonAPI = bot.get('uon')
    await uon.create_user(state_data['name'], state_data['phone'], birthday.isoformat())

    await message.answer(messages.main_menu, reply_markup=reply_keyboards.main_menu)
    await state.finish()


def register_registration(dp: Dispatcher):
    dp.register_message_handler(get_phone, state=states.Registration.waiting_for_phone, content_types=ContentType.CONTACT)
    dp.register_message_handler(get_name, state=states.Registration.waiting_for_name)
