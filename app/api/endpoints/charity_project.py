from fastapi import APIRouter

from app.api.deps import AsyncSessionDep, SuperUserDep
from app.api.validators import (
    check_name_duplicate,
    check_project_before_delete,
    check_project_before_update,
    check_project_exists,
)
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investment import invest

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    summary='Список проектов',
    description='Показать список всех целевых проектов.',
)
async def get_all_charity_projects(session: AsyncSessionDep):
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    summary='Создать проект',
    description='Создать целевой проект.',
)
async def create_charity_project(
    project: CharityProjectCreate,
    session: AsyncSessionDep,
    _superuser: SuperUserDep,
):
    await check_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create(
        project,
        session,
        commit=False,
    )
    await invest(new_project, session)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    summary='Изменить проект',
    description=(
        'Редактировать целевой проект. Закрытый проект нельзя '
        'редактировать; нельзя установить требуемую сумму меньше '
        'уже вложенной.'
    ),
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSessionDep,
    _superuser: SuperUserDep,
):
    project = await check_project_exists(project_id, session)
    await check_project_before_update(project, obj_in, session)
    return await charity_project_crud.update(project, obj_in, session)


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    summary='Удалить проект',
    description=(
        'Удалить целевой проект. Нельзя удалить проект, '
        'в который уже были инвестированы средства.'
    ),
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSessionDep,
    _superuser: SuperUserDep,
):
    project = await check_project_exists(project_id, session)
    check_project_before_delete(project)
    return await charity_project_crud.remove(project, session)
