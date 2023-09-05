from dataclasses import dataclass

from environs import Env


@dataclass
class DatabaseConfig:
    password: str
    user: str
    database: str


@dataclass
class TelegramBot:
    token: str
    admin_ids: list[int]
    write_logs: bool


@dataclass
class Miscellaneous:
    uon_key: str
    salebot_key: str
    salebot_list_id: str
    support_bot_link: str


@dataclass
class Email:
    sender: str
    reveiver: str
    user: str
    password: str


@dataclass
class Config:
    bot: TelegramBot
    database: DatabaseConfig
    misc: Miscellaneous
    email: Email


def load_config(path: str = None):
    env = Env()
    env.read_env('.env')

    return Config(
        bot=TelegramBot(
            token=env.str('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMINS'))),
            write_logs=env.bool('WRITE_LOGS'),
        ),
        database=DatabaseConfig(
            password=env.str('POSTGRES_PASSWORD'),
            user=env.str('POSTGRES_USER'),
            database=env.str('POSTGRES_DB')
        ),
        misc=Miscellaneous(
            uon_key=env.str('UON_KEY'),
            salebot_key=env.str('SALEBOT_KEY'),
            salebot_list_id=env.int('SALEBOT_LIST_ID'),
            support_bot_link=env.str('SUPPORT_BOT_LINK')
        ),
        email=Email(
            sender=env.str('EMAIL_SENDER'),
            reveiver=env.str('EMAIL_RECEIVER'),
            user=env.str('EMAIL_USER'),
            password=env.str('EMAIL_PASSWORD')
        )
    )
