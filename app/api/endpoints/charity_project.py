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
)
async def get_all_charity_projects(session: AsyncSessionDep):
    """Показать все целевые проекты.

    Доступен без регистрации. В список входят и открытые сборы,
    и уже закрытые.

    Для каждого проекта возвращаются:

    * `name` и `description`;
    * `full_amount` — сколько нужно собрать;
    * `invested_amount` — сколько уже вложено;
    * `fully_invested`, `create_date` и `close_date`.
    """
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    summary='Создать проект',
)
async def create_charity_project(
    project: CharityProjectCreate,
    session: AsyncSessionDep,
    _superuser: SuperUserDep,
):
    """Создать целевой проект.

    Доступно только суперпользователю. Название должно быть уникальным,
    от 5 до 100 символов. Описание — не короче 10 символов.
    `full_amount` — целое число больше нуля.

    Если в фонде уже есть нераспределённые пожертвования, они сразу
    вкладываются в новый проект. Создание и распределение сохраняются
    одной транзакцией. В ответе суммы уже с учётом этих вложений.
    """
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
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSessionDep,
    _superuser: SuperUserDep,
):
    """Изменить открытый целевой проект.

    Доступно только суперпользователю. Можно передать любое из полей
    `name`, `description`, `full_amount`.

    Ограничения:

    * закрытый проект менять нельзя;
    * название не должно совпадать с другим проектом;
    * новая требуемая сумма не может быть меньше уже вложенной;
    * если требуемая сумма стала равна вложенной, проект закрывается.
    """
    project = await check_project_exists(project_id, session)
    await check_project_before_update(project, obj_in, session)
    return await charity_project_crud.update(project, obj_in, session)


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    summary='Удалить проект',
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSessionDep,
    _superuser: SuperUserDep,
):
    """Удалить целевой проект.

    Доступно только суперпользователю.

    Удаление запрещено, если в проект уже вносили деньги или он закрыт.
    В ответе возвращается удалённый проект.
    """
    project = await check_project_exists(project_id, session)
    check_project_before_delete(project)
    return await charity_project_crud.remove(project, session)
