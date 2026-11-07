from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from app.core.constants import (
    DESCRIPTION_MIN_LENGTH,
    NAME_MAX_LENGTH,
    NAME_MIN_LENGTH,
)


class CharityProjectCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=NAME_MIN_LENGTH,
        max_length=NAME_MAX_LENGTH,
        title='Название',
        description='Уникальное название проекта, от 5 до 100 символов.',
    )
    description: str = Field(
        ...,
        min_length=DESCRIPTION_MIN_LENGTH,
        title='Описание',
        description='Описание проекта, не короче 10 символов.',
    )
    full_amount: PositiveInt = Field(
        ...,
        title='Требуемая сумма',
        description='Целое число больше нуля.',
    )

    model_config = ConfigDict(extra='forbid')


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=NAME_MIN_LENGTH,
        max_length=NAME_MAX_LENGTH,
        title='Название',
    )
    description: Optional[str] = Field(
        None,
        min_length=DESCRIPTION_MIN_LENGTH,
        title='Описание',
    )
    full_amount: Optional[PositiveInt] = Field(
        None,
        title='Требуемая сумма',
    )

    model_config = ConfigDict(extra='forbid')


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
