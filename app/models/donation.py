from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import InvestmentBase


class Donation(InvestmentBase):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text)

    def __repr__(self):
        return (
            f'{type(self).__name__}('
            f'id={self.id}, user_id={self.user_id}, '
            f'full_amount={self.full_amount}, '
            f'invested_amount={self.invested_amount}, '
            f'fully_invested={self.fully_invested})'
        )
