import datetime

from sqlalchemy import Column, BigInteger, DateTime, String, Boolean, ForeignKey, Text, select, Integer, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from tgbot.misc.other import MONTHS
from tgbot.services.database.base import Base


class TourPickup(Base):
    __tablename__ = 'tour_pickup'

    id = Column(Integer, primary_key=True, autoincrement=True)
    departure_city = Column(String(64))
    country = Column(String(64))
    adults_count = Column(Integer)
    kids_count = Column(Integer)
    kids_ages = Column(String(255))
    hotel_stars = Column(Integer)
    food_type = Column(String(32))
    date = Column(Date)
    night_count = Column(String(16))
    telegram_user_id = Column(ForeignKey('telegram_user.telegram_id'))

    telegram_user = relationship('TelegramUser', backref='pickup_tours')
