import datetime

from sqlalchemy import Column, BigInteger, DateTime, String, Boolean, ForeignKey, Text, select, Integer, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from tgbot.misc.other import MONTHS
from tgbot.services.database.base import Base


class AuthorTourRequest(Base):
    __tablename__ = 'author_tour_request'

    id = Column(Integer, primary_key=True, autoincrement=True)
    author_tour_id = Column(Integer, ForeignKey('author_tour.id'))
    user_id = Column(BigInteger, ForeignKey('telegram_user.telegram_id'))
    month = Column(String(10))
    created_at = Column(DateTime)

    author_tour = relationship('AuthorTour')
    telegram_user = relationship('TelegramUser')
