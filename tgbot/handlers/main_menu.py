from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from tgbot.misc import reply_commands


async def start_tour_pickup(message: Message):
    await message.answer('В разработке!')


async def send_account(message: Message):
    await message.answer('В разработке!')


async def send_author_tours(message: Message):
    await message.answer('В разработке!')


async def start_question_input(message: Message):
    await message.answer('В разработке!')


def register_main_menu(dp: Dispatcher):
    dp.register_message_handler(start_tour_pickup, Text(equals=reply_commands.tour_pickup))
    dp.register_message_handler(send_account, Text(equals=reply_commands.account))
    dp.register_message_handler(send_author_tours, Text(equals=reply_commands.author_tours))
    dp.register_message_handler(start_question_input, Text(equals=reply_commands.make_question))
