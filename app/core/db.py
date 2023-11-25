from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, false, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings


class PreBase:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)


class Charity(Base):
    """ Родительский класс для таблиц проектов и пожертвований """

    __abstract__ = True

    full_amount = Column(Integer)
    invested_amount = Column(Integer, server_default='0')
    fully_invested = Column(Boolean, server_default=false())
    create_date = Column(DateTime, default=datetime.utcnow)
    close_date = Column(DateTime)

    @hybrid_property
    def remains(self):
        return self.full_amount - self.invested_amount


engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session
