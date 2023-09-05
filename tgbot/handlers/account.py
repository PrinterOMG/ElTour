from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot.config import Config
from tgbot.handlers.main_menu import send_account
from tgbot.keyboards import inline_keyboards, reply_keyboards
from tgbot.misc import callbacks, messages, states
from tgbot.services.database.models import TelegramUser
from tgbot.services.salebot import SalebotAPI


async def show_account(call: CallbackQuery):
    db = call.bot.get('database')
    async with db() as session:
        tg_user = await session.get(TelegramUser, call.from_user.id)

    await call.message.edit_text(
        messages.account.format(phone=tg_user.phone, name=tg_user.name, mailing=tg_user.pretty_mailing(),
                                birthday=tg_user.birthday.isoformat() if tg_user.birthday else 'Не указан'),
        reply_markup=inline_keyboards.account
    )
    await call.answer()


async def switch_mailing(call: CallbackQuery):
    db = call.bot.get('database')
    async with db.begin() as session:
        tg_user = await session.get(TelegramUser, call.from_user.id)
        tg_user.mailing_sub = not tg_user.mailing_sub

    config: Config = call.bot.get('config')
    salebot: SalebotAPI = call.bot.get('salebot')
    if tg_user.mailing_sub:
        await salebot.add_to_list(tg_user.salebot_id, config.misc.salebot_list_id)
    else:
        await salebot.remove_from_list(tg_user.salebot_id, config.misc.salebot_list_id)

    await show_account(call)


async def start_name_update(call: CallbackQuery):
    await states.NameUpdate.first()
    await call.message.answer(messages.name_update, reply_markup=reply_keyboards.cancel)
    await call.answer()


async def get_new_name(message: Message, state: FSMContext):
    new_name = message.text

    if len(new_name) > 32:
        await message.answer(messages.long_name)
        return

    db = message.bot.get('database')
    async with db.begin() as session:
        tg_user = await session.get(TelegramUser, message.from_id)
        tg_user.name = new_name

    await state.finish()
    await message.answer(messages.name_updated.format(new_name=new_name), reply_markup=reply_keyboards.main_menu)
    await send_account(message)


def register_account(dp: Dispatcher):
    dp.register_callback_query_handler(switch_mailing, callbacks.account.filter(action='switch_mailing'))
    dp.register_callback_query_handler(start_name_update, callbacks.account.filter(action='update_name'))
    dp.register_message_handler(get_new_name, state=states.NameUpdate.waiting_for_name)
