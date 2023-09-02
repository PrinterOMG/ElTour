from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from tgbot.handlers.main_menu import send_account
from tgbot.keyboards import reply_keyboards
from tgbot.misc import states, messages, reply_commands


async def cancel(message: Message, state: FSMContext):
    cur_state = await state.get_state()
    if cur_state in states.NameUpdate:
        await message.answer('Отменено!', reply_markup=reply_keyboards.main_menu)
        await send_account(message)
    else:
        await message.answer(messages.main_menu, reply_markup=reply_keyboards.main_menu)

    await state.finish()


async def pass_call(call: CallbackQuery):
    await call.answer()


def register_other(dp: Dispatcher):
    dp.register_message_handler(cancel, Text(equals=reply_commands.cancel), state='*')
    dp.register_callback_query_handler(pass_call, text='pass', state='*')
