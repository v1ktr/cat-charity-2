from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation


def _prepare(obj):
    if obj.invested_amount is None:
        obj.invested_amount = 0
    if obj.fully_invested is None:
        obj.fully_invested = False


def _close_if_full(obj):
    if obj.invested_amount >= obj.full_amount:
        obj.fully_invested = True
        obj.close_date = datetime.now()


def _transfer(source, target):
    free_amount = source.full_amount - source.invested_amount
    need_amount = target.full_amount - target.invested_amount
    amount = min(free_amount, need_amount)
    if amount <= 0:
        _close_if_full(target)
        return
    source.invested_amount += amount
    target.invested_amount += amount
    _close_if_full(source)
    _close_if_full(target)


async def _open_targets(obj, session: AsyncSession):
    model = Donation if isinstance(obj, CharityProject) else CharityProject
    result = await session.execute(
        select(model).where(
            model.fully_invested.is_(False),
        ).order_by(model.create_date, model.id),
    )
    return result.scalars().all()


async def invest(obj, session: AsyncSession):
    """Распределить свободные суммы. Коммит — один, в конце."""
    _prepare(obj)
    session.add(obj)
    with session.no_autoflush:
        targets = await _open_targets(obj, session)
        for target in targets:
            _transfer(obj, target)
            if obj.fully_invested:
                break
    await session.commit()
    await session.refresh(obj)
