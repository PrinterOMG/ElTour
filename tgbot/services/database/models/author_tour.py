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
    month = Column(String(3))
    year = Column(Integer)
    description = Column(Text)
    landing_url = Column(String(255))
    image_url = Column(String(255))
    image_tg_id = Column(String(255))

    country = relationship('Country', lazy='selectin')

    def pretty_month(self):
        return MONTHS[self.month]

    def pretty_date(self):
        return f'{self.pretty_month()} {self.year}'

    @classmethod
    async def get_by_country(cls, session, country_id):
        stmt = select(AuthorTour).where(AuthorTour.country_id == int(country_id))
        records = await session.execute(stmt)

        return records.scalars().all()
