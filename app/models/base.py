from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Integer,
)
from sqlalchemy.orm import declared_attr

from app.core.constants import DEFAULT_INVESTED_AMOUNT
from app.core.db import Base


class InvestmentBase(Base):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @declared_attr
    def __table_args__(cls):
        table = cls.__name__.lower()
        return (
            CheckConstraint(
                'full_amount > 0',
                name=f'ck_{table}_full_amount_positive',
            ),
            CheckConstraint(
                'invested_amount <= full_amount',
                name=f'ck_{table}_invested_le_full_amount',
            ),
        )

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(
        Integer,
        nullable=False,
        default=DEFAULT_INVESTED_AMOUNT,
    )
    fully_invested = Column(Boolean, nullable=False, default=False)
    create_date = Column(DateTime, nullable=False, default=datetime.now)
    close_date = Column(DateTime)

    def __repr__(self):
        return (
            f'{type(self).__name__}('
            f'id={self.id}, '
            f'full_amount={self.full_amount}, '
            f'invested_amount={self.invested_amount}, '
            f'fully_invested={self.fully_invested})'
        )
