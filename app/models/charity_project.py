from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, false, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property

from app.core.db import Base


class CharityProject(Base):
    """ Модель проекта для пожертвований """
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String, nullable=False)
    full_amount = Column(Integer)
    invested_amount = Column(Integer, server_default='0')
    fully_invested = Column(Boolean, server_default=false())
    create_date = Column(DateTime, default=datetime.utcnow)
    close_date = Column(DateTime)

    @hybrid_property
    def needed_amount(self):
        return self.full_amount - self.invested_amount
