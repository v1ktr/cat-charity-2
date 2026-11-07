from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import (
    FULL_AMOUNT_TOO_LOW,
    NAME_DUPLICATE,
    PROJECT_CLOSED,
    PROJECT_INVESTED,
    PROJECT_NOT_FOUND,
)
from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_id_by_name(
        project_name,
        session,
    )
    if project_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=NAME_DUPLICATE,
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=PROJECT_NOT_FOUND,
        )
    return project


def check_project_before_delete(project: CharityProject) -> None:
    invested = project.fully_invested or project.invested_amount > 0
    if invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=PROJECT_INVESTED,
        )


async def check_project_before_update(
    project: CharityProject,
    obj_in: CharityProjectUpdate,
    session: AsyncSession,
) -> None:
    if project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=PROJECT_CLOSED,
        )
    await _check_name(project, obj_in, session)
    _check_full_amount(project, obj_in)


async def _check_name(project, obj_in, session: AsyncSession) -> None:
    name_changed = obj_in.name is not None and obj_in.name != project.name
    if name_changed:
        await check_name_duplicate(obj_in.name, session)


def _check_full_amount(project, obj_in) -> None:
    new_amount = obj_in.full_amount
    if new_amount is not None and new_amount < project.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=FULL_AMOUNT_TOO_LOW,
        )
