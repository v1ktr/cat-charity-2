from sqlalchemy import Column, String, Text

from app.core.constants import NAME_MAX_LENGTH
from app.models.base import InvestmentBase


class CharityProject(InvestmentBase):
    name = Column(String(NAME_MAX_LENGTH), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            f'{type(self).__name__}('
            f'id={self.id}, name={self.name!r}, '
            f'full_amount={self.full_amount}, '
            f'invested_amount={self.invested_amount}, '
            f'fully_invested={self.fully_invested})'
        )
