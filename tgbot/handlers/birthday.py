from datetime import datetime

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.keyboards import reply_keyboards
from tgbot.misc import messages, states
from tgbot.services.database.models import TelegramUser
from tgbot.services.uon import UonAPI


async def get_birthday(message: Message, state: FSMContext):
    birthday = message.text

    try:
        birthday = datetime.strptime(birthday, '%d.%m.%Y')
    except ValueError:
        await message.answer(messages.bad_birthday)
        return

    db = message.bot.get('database')
    async with db.begin() as session:
        tg_user = await session.get(TelegramUser, message.from_id)
        tg_user.birthday = birthday.date()

    await message.answer(messages.birthday_ok, reply_markup=reply_keyboards.main_menu)
    await state.finish()

    uon: UonAPI = message.bot.get('uon')
    await uon.update_birthday(tg_user.phone, birthday.isoformat())


def register_birthday(dp: Dispatcher):
    dp.register_message_handler(get_birthday, state=states.Birthday.waiting_for_birthday)
