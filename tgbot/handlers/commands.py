from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.keyboards import reply_keyboards
from tgbot.misc import messages, states

from tgbot.services.database.models import TelegramUser


async def command_start(message: Message):
    db = message.bot.get('database')
    async with db() as session:
        tg_user = await session.get(TelegramUser, message.from_id)
        if not tg_user:
            await message.answer(messages.phone_request, reply_markup=reply_keyboards.phone_request)
            await states.Registration.first()
        else:
            await message.answer(messages.main_menu, reply_markup=reply_keyboards.main_menu)


def register_commands(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'], state='*')
