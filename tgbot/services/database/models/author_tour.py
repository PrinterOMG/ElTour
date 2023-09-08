import datetime

from sqlalchemy import Column, BigInteger, DateTime, String, Boolean, ForeignKey, Text, select, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from tgbot.misc.other import MONTHS
from tgbot.services.database.base import Base


class AuthorTour(Base):
    __tablename__ = 'author_tour'

    id = Column(Integer, primary_key=True, autoincrement=True)
    country_id = Column(ForeignKey('country.id'))
    month = Column(String(255))
    year = Column(Integer)
    description = Column(Text)
    landing_url = Column(String(255))
    image_url = Column(Text)
    image_tg_id = Column(String(255))

    country = relationship('Country', lazy='selectin')

    @classmethod
    async def get_by_country(cls, session, country_id):
        stmt = select(AuthorTour).where(AuthorTour.country_id == int(country_id))
        records = await session.execute(stmt)

        return records.scalars().all()

    @classmethod
    async def get_countries(cls, session):
        stmt = select(AuthorTour)
        records = await session.execute(stmt)

        return {tour.country for tour in records.scalars().all()}
