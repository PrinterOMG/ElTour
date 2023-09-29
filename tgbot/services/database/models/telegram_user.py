import datetime

from sqlalchemy import Column, BigInteger, DateTime, String, Boolean, Date
from sqlalchemy.sql.expression import text

from tgbot.services.database.base import Base


class TelegramUser(Base):
    __tablename__ = 'telegram_user'

    telegram_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    phone = Column(String(16))
    name = Column(String(32))
    birthday = Column(Date)
    full_name = Column(String(128))
    mention = Column(String(128))
    mailing_sub = Column(Boolean, default=True)
    created_at = Column(DateTime())
    salebot_id = Column(BigInteger)

    def pretty_mailing(self):
        return 'Включена' if self.mailing_sub else 'Выключена'
