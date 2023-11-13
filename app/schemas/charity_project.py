from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator, PositiveInt


class CharityProjectBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        title='Название проекта'
    )
    description: str = Field(
        ...,
        min_length=1,
        title='Описание проекта'
    )
    full_amount: PositiveInt = Field(
        ...,
        title='Требуемая сумма'
    )


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: Optional[int] = 0
    fully_invested: Optional[bool] = False
    create_date: datetime
    close_date: Optional[datetime] = Field(None)

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase, extra=Extra.forbid):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt] = Field(None)

    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Поле "name" не может быть пустым!')
        return value

    @validator('description')
    def description_cannot_be_empty(cls, value):
        if value == '':
            raise ValueError(
                'Поле "description" не может быть пустой строкой!'
            )
        return value
