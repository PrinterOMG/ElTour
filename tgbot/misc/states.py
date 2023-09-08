from aiogram.dispatcher.filters.state import StatesGroup, State


class Registration(StatesGroup):
    waiting_for_phone = State()
    waiting_for_name = State()


class NameUpdate(StatesGroup):
    waiting_for_name = State()


class TourPickup(StatesGroup):
    waiting_for_city = State()
    waiting_for_country = State()
    waiting_for_adult_count = State()
    waiting_for_kids_count = State()
    waiting_for_kids_age = State()
    waiting_for_hotel_stars = State()
    waiting_for_food_type = State()
    waiting_for_date = State()
    waiting_for_nights_count = State()

    finishing = State()


class Birthday(StatesGroup):
    waiting_for_birthday = State()
