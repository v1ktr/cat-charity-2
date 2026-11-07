from sqlalchemy import Column, String, Text

from app.models.base import InvestmentBase


class CharityProject(InvestmentBase):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
