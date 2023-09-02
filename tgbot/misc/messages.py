from tgbot.misc import reply_commands


main_menu = (
    'Главное меню'
)

phone_request = (
    f'Нажмите кнопку "{reply_commands.phone_request}"'
)

not_your_phone = (
    f'Это не ваш контакт! Нажмите кнопку "{reply_commands.phone_request}"'
)

name_input = (
    'Хорошо! Теперь отправьте как вас зовут'
)

long_name = (
    'Имя слишком длинное! Отправьте имя покороче'
)

account = (
    'Личный кабинет\n\n'
    'Ваше имя: {name}\n'
    'Ваш номер: {phone}\n\n'
    'Рассылка: {mailing}'
)

name_update = (
    'Отправьте новое имя'
)

name_updated = (
    'Имя обновлено на {new_name}!'
)

author_tour_intro = (
    'Уже много лет мы организовываем авторские туры в разные страны мира.\n\n'
    'Выберите направление'
)

author_tour_choose = (
    'Направление - {country}\n\n'
    'Выберите дату'
)

author_tour = (
    'Авторский тур\n\n'
    'Направление - {country}\n'
    'Дата - {date}\n'
    'Описание:\n'
    '{description}'
)

departure_city_input = (
    'Выберите город вылета.\n'
    'Если нужного города нет, отправьте его сообщением'
)

tour_country_input = (
    'Город вылета: {departure_city}\n\n'
    'Выберите куда хотите отправиться в путешествие.\n'
    'Если нужной страны нет, отправьте её сообщением'
)

adults_count_input = (
    'Страна для путешествия: {tour_country}\n\n'
    'Выберите количество взрослых.\n'
    'Если нужного количества нет, отправьте его сообщением'
)

kids_count_input = (
    'Количество взрослых: {adults_count}\n\n'
    'Выберите количество детей.\n'
    'Если нужного количества нет, отправьте его сообщением'
)

kids_age_input = (
    'Количество детей: {kids_count}\n\n'
    'Выберите возраст {kid_num}-го ребенка'
)

hotel_stars_input = (
    'Количество детей: {kids_count}\n\n'
    'Выберите категорию отеля'
)

food_type_input = (
    'Категория отеля: {hotel_stars}\n\n'
    'Выберите тип питания'
)

date_input = (
    'Тип питания: {food_type}\n\n'
    'Выберите дату вылета'
)

old_date = (
    'Нельзя выбрать прошедшею дату!'
)

nights_count_input = (
    'Дата вылета: {date}\n\n'
    'Выберите количество ночей'
)

tour_pickup_confirmation = (
    'Описание заявки\n\n'
    '---\n\n'
    'Страна для путешествия: {country}\n\n'
    'Количество взрослых: {adults_count}\n\n'
    'Количество детей: {kids_count}\n'
    '{kids_age}'
    'Категория отеля: {hotel_stars}\n\n'
    'Тип питания: {food_type}\n\n'
    'Количество ночей: {nights_count}\n\n'
    'Город вылета: {city}\n'
    'Дата вылета: {date}'
)

tour_pickup_hint = (
    f'Нажмите кнопку "{reply_commands.back}" для возврата к предыдущему пункту\n'
    f'Нажмите кнопку "{reply_commands.start_over}" для заполнения формы заново\n'
    f'Нажмите кнопку "{reply_commands.cancel}" для отмены'
)
