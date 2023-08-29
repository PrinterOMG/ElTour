from aiogram.utils.callback_data import CallbackData


# action: 'update_name', 'switch_mailing'
account = CallbackData('account', 'action')

country = CallbackData('country', 'id')

# action: 'show', 'request'
author_tour = CallbackData('author_tour', 'action', 'id')
