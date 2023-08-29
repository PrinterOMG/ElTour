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
