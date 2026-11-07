from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings

OPENAPI_TAGS = [
    {
        'name': 'Проекты',
        'description': (
            'Целевые сборы: открытие, просмотр, '
            'изменение и удаление проектов.'
        ),
    },
    {
        'name': 'Пожертвования',
        'description': (
            'Пожертвования пользователей и их распределение '
            'по открытым проектам.'
        ),
    },
    {
        'name': 'Аутентификация',
        'description': 'Регистрация, вход и выход из системы.',
    },
    {
        'name': 'Пользователи',
        'description': (
            'Профиль текущего пользователя и управление '
            'учётными записями.'
        ),
    },
]

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version='1.0.0',
    openapi_tags=OPENAPI_TAGS,
)

app.include_router(main_router)
