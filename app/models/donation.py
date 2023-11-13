from datetime import datetime

from sqlalchemy import (
    Boolean, Column, DateTime, false, ForeignKey, Integer, Text
)
from sqlalchemy.ext.hybrid import hybrid_property

from app.core.db import Base


class Donation(Base):
    """ Модель пожертвования """
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
    full_amount = Column(Integer)
    invested_amount = Column(Integer, server_default='0')
    fully_invested = Column(Boolean, server_default=false())
    create_date = Column(DateTime, default=datetime.utcnow)
    close_date = Column(DateTime)

    @hybrid_property
    def available(self):
        return self.full_amount - self.invested_amount
