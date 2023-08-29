import datetime

from sqlalchemy import Column, BigInteger, DateTime, String, Boolean, select, Integer
from sqlalchemy.sql.expression import text

from tgbot.services.database.base import Base


class Country(Base):
    __tablename__ = 'country'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64))

    @classmethod
    async def get_all(cls, session):
        stmt = select(Country)
        records = await session.execute(stmt)

        return records.scalars().all()

