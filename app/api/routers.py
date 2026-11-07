from fastapi import APIRouter

from app.api.endpoints.charity_project import router as project_router
from app.api.endpoints.donation import router as donation_router
from app.api.endpoints.user import router as user_router

main_router = APIRouter()

main_router.include_router(
    project_router,
    prefix='/charity_project',
    tags=['Проекты'],
)
main_router.include_router(
    donation_router,
    prefix='/donation',
    tags=['Пожертвования'],
)
main_router.include_router(user_router)
