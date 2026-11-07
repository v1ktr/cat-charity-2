from fastapi import APIRouter

from app.api.deps import AsyncSessionDep, SuperUserDep, UserDep
from app.crud.donation import donation_crud
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationFullInfoDB,
)
from app.services.investment import invest

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationFullInfoDB],
    summary='Список пожертвований',
    description='Показать список всех пожертвований.',
)
async def get_all_donations(
    session: AsyncSessionDep,
    _superuser: SuperUserDep,
):
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    summary='Мои пожертвования',
    description='Показать пожертвования текущего пользователя.',
)
async def get_my_donations(
    session: AsyncSessionDep,
    user: UserDep,
):
    return await donation_crud.get_by_user(user.id, session)


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    summary='Создать пожертвование',
    description='Создать пожертвование.',
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSessionDep,
    user: UserDep,
):
    new_donation = await donation_crud.create(
        donation,
        session,
        commit=False,
        user_id=user.id,
    )
    await invest(new_donation, session)
    return new_donation
