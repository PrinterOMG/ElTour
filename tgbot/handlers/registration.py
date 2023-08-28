from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType, ReplyKeyboardRemove

from tgbot.keyboards import reply_keyboards
from tgbot.misc import states, messages
from tgbot.services.database.models import TelegramUser


async def get_phone(message: Message, state: FSMContext):
    contact = message.contact

    if message.from_id != contact.user_id:
        await message.answer(messages.not_your_phone, reply_markup=reply_keyboards.phone_request)
        return

    await state.update_data(phone=contact.phone_number.replace('+', ''))
    await message.answer(messages.name_input, reply_markup=ReplyKeyboardRemove())
    await states.Registration.next()


async def get_name(message: Message, state: FSMContext):
    name = message.text

    if len(name) > 32:
        await message.answer(messages.long_name)
        return

    db = message.bot.get('database')
    state_data = await state.get_data()
    async with db.begin() as session:
        new_user = TelegramUser(
            telegram_id=message.from_id,
            name=name,
            full_name=message.from_user.full_name,
            mention=message.from_user.mention,
            phone=state_data['phone']
        )
        session.add(new_user)

    await message.answer(messages.main_menu, reply_markup=reply_keyboards.main_menu)
    await state.finish()


def register_registration(dp: Dispatcher):
    dp.register_message_handler(get_phone, state=states.Registration.waiting_for_phone, content_types=ContentType.CONTACT)
    dp.register_message_handler(get_name, state=states.Registration.waiting_for_name)
