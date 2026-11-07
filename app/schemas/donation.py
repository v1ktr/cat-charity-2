from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, PositiveInt


class DonationCreate(BaseModel):
    full_amount: PositiveInt = Field(
        ...,
        title='Сумма пожертвования',
        description='Целое число больше нуля.',
    )
    comment: Optional[str] = Field(
        None,
        title='Комментарий',
    )

    model_config = ConfigDict(extra='forbid')


class DonationDB(BaseModel):
    id: int
    comment: Optional[str]
    full_amount: PositiveInt
    create_date: datetime

    model_config = ConfigDict(from_attributes=True)


class DonationFullInfoDB(DonationDB):
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
    user_id: int
