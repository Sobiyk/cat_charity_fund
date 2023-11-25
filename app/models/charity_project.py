from datetime import datetime

from sqlalchemy import Column, event, String
from sqlalchemy.ext.hybrid import hybrid_property

from app.core.db import Charity


class CharityProject(Charity):
    """ Модель проекта для пожертвований """
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String, nullable=False)

    @hybrid_property
    def comp_rate(self):
        return self.close_date - self.create_date


@event.listens_for(CharityProject.invested_amount, 'set')
def after_invested_equals_full(target, value, oldvalue, initiator):
    if value == target.full_amount:
        target.close_date = datetime.utcnow()
        target.fully_invested = True
