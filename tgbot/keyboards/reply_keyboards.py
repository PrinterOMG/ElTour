from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.misc import reply_commands


phone_request = ReplyKeyboardMarkup(resize_keyboard=True)
phone_request.add(
    KeyboardButton(reply_commands.phone_request, request_contact=True)
)

main_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
main_menu.add(
    KeyboardButton(reply_commands.tour_pickup),
    KeyboardButton(reply_commands.author_tours),
    KeyboardButton(reply_commands.make_question),
    KeyboardButton(reply_commands.account)
)

cancel = ReplyKeyboardMarkup(resize_keyboard=True)
cancel.add(
    KeyboardButton(reply_commands.cancel)
)
