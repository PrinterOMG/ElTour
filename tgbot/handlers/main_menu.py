from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from tgbot.keyboards import inline_keyboards
from tgbot.misc import reply_commands, messages
from tgbot.services.database.models import TelegramUser


async def start_tour_pickup(message: Message):
    await message.answer('В разработке!')


async def send_account(message: Message):
    db = message.bot.get('database')
    async with db() as session:
        tg_user = await session.get(TelegramUser, message.from_id)

    await message.answer(
        messages.account.format(phone=tg_user.phone, name=tg_user.name, mailing=tg_user.pretty_mailing()),
        reply_markup=inline_keyboards.account
    )


async def send_author_tours(message: Message):
    await message.answer('В разработке!')


async def start_question_input(message: Message):
    await message.answer('В разработке!')


def register_main_menu(dp: Dispatcher):
    dp.register_message_handler(start_tour_pickup, Text(equals=reply_commands.tour_pickup))
    dp.register_message_handler(send_account, Text(equals=reply_commands.account))
    dp.register_message_handler(send_author_tours, Text(equals=reply_commands.author_tours))
    dp.register_message_handler(start_question_input, Text(equals=reply_commands.make_question))
