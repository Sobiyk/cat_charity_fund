from datetime import datetime

from sqlalchemy import Column, event, ForeignKey, Integer, Text

from app.core.db import Charity


class Donation(Charity):
    """ Модель пожертвования """
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)


@event.listens_for(Donation.invested_amount, 'set')
def after_invested_equals_full(target, value, oldvalue, initiator):
    if value == target.full_amount:
        target.close_date = datetime.utcnow()
        target.fully_invested = True
