from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.misc import callbacks


account = InlineKeyboardMarkup(row_width=1)
account.add(
    InlineKeyboardButton('Изменить имя', callback_data=callbacks.account.new('update_name')),
    InlineKeyboardButton('Вкл/выкл рассылку', callback_data=callbacks.account.new('switch_mailing'))
)
