import datetime
from pprint import pprint

from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType, ReplyKeyboardRemove

from tgbot.config import Config
from tgbot.keyboards import reply_keyboards
from tgbot.misc import states, messages
from tgbot.services.database.models import TelegramUser
from tgbot.services.salebot import SalebotAPI
from tgbot.services.uon import UonAPI


async def get_name(message: Message, state: FSMContext):
    name = message.text

    if len(name) > 32:
        await message.answer(messages.long_name)
        return

    bot = Bot.get_current()

    config: Config = message.bot.get('config')
    salebot: SalebotAPI = message.bot.get('salebot')
    bot_info = await message.bot.me
    clients = await salebot.load_client(bot_info.username, message.from_id)
    clients = clients.get('items')
    salebot_id = clients[0].get('id') if clients else None
    if salebot_id:
        await salebot.add_to_list(salebot_id, config.misc.salebot_list_id)

    db = bot.get('database')
    async with db.begin() as session:
        new_user = TelegramUser(
            telegram_id=message.from_id,
            name=name,
            full_name=message.from_user.full_name,
            mention=message.from_user.mention,
            salebot_id=salebot_id
        )
        session.add(new_user)

    await message.answer(messages.main_menu, reply_markup=reply_keyboards.main_menu)
    await state.finish()


def register_registration(dp: Dispatcher):
    dp.register_message_handler(get_name, state=states.Registration.waiting_for_name)
