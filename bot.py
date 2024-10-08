import asyncio
import datetime
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.utils.exceptions import CantGetUpdates
from aioredis import Redis
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tgbot.config import load_config
from tgbot import handlers
from tgbot import filters
from tgbot import middlewares
from tgbot.services.salebot import SalebotAPI
from tgbot.services.uon import UonAPI

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config):
    dp.setup_middleware(middlewares.EnvironmentMiddleware(config=config))
    dp.setup_middleware(middlewares.ThrottlingMiddleware())


def register_all_filters(dp):
    for aiogram_filter in filters.filters:
        dp.filters_factory.bind(aiogram_filter)


def register_all_handlers(dp):
    for register in handlers.register_functions:
        register(dp)


async def main():
    config = load_config('.env')
    logging_handlers = [logging.StreamHandler()]
    if config.bot.write_logs:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        log_file = rf'logs/{datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")}.log'
        logging_handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
        handlers=logging_handlers
    )
    logger.info('Starting bot')

    bot = Bot(token=config.bot.token, parse_mode='HTML')
    bot_info = await bot.me
    logger.info(f'Bot: {bot_info.username} [{bot_info.mention}]')

    storage = RedisStorage2(host='localhost')
    dp = Dispatcher(bot, storage=storage)
    redis = Redis(host='localhost')

    uon = UonAPI(config.misc.uon_key)
    salebot = SalebotAPI(config.misc.salebot_key)

    engine = create_async_engine(
        f'postgresql+asyncpg://{config.database.user}:{config.database.password}@127.0.0.1/{config.database.database}',
        future=True
    )
    async_sessionmaker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession, future=True)

    bot['config'] = config
    bot['redis'] = redis
    bot['database'] = async_sessionmaker
    bot['uon'] = uon
    bot['salebot'] = salebot

    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)

    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(
        func=bot.delete_webhook,
        trigger='interval',
        minutes=10
    )
    scheduler.start()

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()

        bot_session = await bot.get_session()
        await bot_session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit) as e:
        logger.error('Bot stopped!')
        raise e
