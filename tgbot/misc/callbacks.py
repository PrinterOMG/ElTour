from aiogram.utils.callback_data import CallbackData


# action: 'update_name', 'switch_mailing'
account = CallbackData('account', 'action')

country = CallbackData('country', 'id')

# action: 'show', 'request'
author_tour = CallbackData('author_tour', 'action', 'id')

city_pickup = CallbackData('city', 'name')

country_pickup = CallbackData('country_pickup', 'name')

adults_count = CallbackData('adults_count', 'count')

kids_count = CallbackData('kids_count', 'count')

kid_age = CallbackData('kid_age', 'age')

hotel_stars = CallbackData('hotel_stars', 'stars')

food_type = CallbackData('food_type', 'type')

# actions: 'show', 'select'
# if action == 'show' value contains str in format '{year} {month}'
# if action == 'select' value contains date timestamp
calendar = CallbackData('calendar', 'action', 'value')  # ???

nights_count = CallbackData('nights_count', 'count')

# actions: 'confirm', 'update'
tour_pickup = CallbackData('tour_pickup', 'action', 'payload')
