from datetime import datetime

from sqlalchemy import Column, event, String

from app.core.db import Charity


class CharityProject(Charity):
    """ Модель проекта для пожертвований """
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String, nullable=False)


@event.listens_for(CharityProject.invested_amount, 'set')
def after_invested_equals_full(target, value, oldvalue, initiator):
    if value == target.full_amount:
        target.close_date = datetime.utcnow()
        target.fully_invested = True
