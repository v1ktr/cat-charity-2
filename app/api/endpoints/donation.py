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
)
async def get_all_donations(
    session: AsyncSessionDep,
    _superuser: SuperUserDep,
):
    """Показать все пожертвования фонда.

    Доступно только суперпользователю. В отличие от ответа
    для обычного пользователя, здесь видны служебные поля:

    * `invested_amount` и `fully_invested`;
    * `close_date`;
    * `user_id` — кто внёс пожертвование.
    """
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    summary='Мои пожертвования',
)
async def get_my_donations(
    session: AsyncSessionDep,
    user: UserDep,
):
    """Показать пожертвования текущего пользователя.

    Нужна авторизация. Чужие пожертвования в ответ не попадают.

    Возвращаются только `id`, `full_amount`, `comment` и `create_date`.
    Пустой комментарий в ответ не включается.
    """
    return await donation_crud.get_by_user(user.id, session)


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    summary='Создать пожертвование',
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSessionDep,
    user: UserDep,
):
    """Сделать пожертвование в фонд.

    Нужна авторизация. Деньги отправляются фонду, а не в выбранный
    проект: сумма вкладывается в самый старый открытый проект.
    Если её больше, чем проекту не хватает, остаток переходит
    к следующему. Нет открытых проектов — сумма ждёт новый сбор.

    Обязательно поле `full_amount` (целое число больше нуля).
    `comment` можно не передавать.

    Создание и распределение сохраняются одной транзакцией.
    """
    new_donation = await donation_crud.create(
        donation,
        session,
        commit=False,
        user_id=user.id,
    )
    await invest(new_donation, session)
    return new_donation
