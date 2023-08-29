import datetime

from aiogram.types.base import Integer
from sqlalchemy import Column, BigInteger, DateTime, String, Boolean
from sqlalchemy.sql.expression import text

from tgbot.services.database.base import Base


class Country(Base):
    __tablename__ = 'country'

    id = Column(Integer, primary_key=True, autoincremen=True)
    name = Column(String(64))
