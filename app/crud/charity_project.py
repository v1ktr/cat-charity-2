from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ):
        project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name,
            ),
        )
        return project_id.scalars().first()

    async def update(self, db_obj, obj_in, session: AsyncSession):
        update_data = obj_in.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        if db_obj.full_amount == db_obj.invested_amount:
            db_obj.fully_invested = True
            db_obj.close_date = datetime.now()
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


charity_project_crud = CRUDCharityProject(CharityProject)
