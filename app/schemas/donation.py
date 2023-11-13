from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class DonationBase(BaseModel):
    comment: Optional[str] = Field(None)
    full_amount: PositiveInt


class DonationCreate(DonationBase):
    pass


class DonationDBUser(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDBAdmin(DonationDBUser):
    user_id: int
    invested_amount: Optional[int] = 0
    fully_invested: Optional[bool] = False
    close_date: Optional[datetime] = Field(None)
