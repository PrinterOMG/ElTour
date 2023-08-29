import datetime

from aiogram.types.base import Integer
from sqlalchemy import Column, BigInteger, DateTime, String, Boolean, ForeignKey, Text, select
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from tgbot.services.database.base import Base


class AuthorTour(Base):
    __tablename__ = 'author_tour'

    id = Column(Integer, primary_key=True, autoincremen=True)
    country_id = Column(ForeignKey('country.id'))
    month = Column(String(3))
    year = Column(Integer)
    description = Column(Text)
    landing_url = Column(String(255))
    image_url = Column(String(255))
    image_tg_id = Column(String(255))

    country = relationship('Country', lazy='selectin')

    @classmethod
    async def get_all(cls, session):
        stmt = select(AuthorTour)
        records = await session.execute(stmt)

        return records.scalars().all()
