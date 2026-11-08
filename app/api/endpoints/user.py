import inspect

from fastapi import APIRouter

from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()


def _document(api_router, route_name, docstring):
    """Прописать описание эндпоинта fastapi-users для кода и Swagger."""
    text = inspect.cleandoc(docstring)
    for route in api_router.routes:
        if getattr(route, 'name', None) != route_name:
            continue
        route.endpoint.__doc__ = text
        route.description = text
        return


auth_router = fastapi_users.get_auth_router(auth_backend)
_document(
    auth_router,
    'auth:jwt.login',
    """
    Войти и получить JWT.

    Тело запроса — форма `application/x-www-form-urlencoded`:

    * `username` — электронная почта;
    * `password` — пароль.

    В ответе `access_token` и `token_type`.
    Дальше токен передаётся как `Authorization: Bearer <token>`.
    """,
)
_document(
    auth_router,
    'auth:jwt.logout',
    """
    Выйти из системы.

    Нужен действующий JWT. Токен сам по себе остаётся валидным
    до истечения срока: сервер не хранит сессии.
    При успехе ответ пустой, статус `204`.
    """,
)
router.include_router(
    auth_router,
    prefix='/auth/jwt',
    tags=['Аутентификация'],
)

register_router = fastapi_users.get_register_router(UserRead, UserCreate)
_document(
    register_router,
    'register:register',
    """
    Зарегистрировать пользователя.

    Обязательны `email` и `password`. Пароль не короче 3 символов
    и не должен содержать адрес почты.

    Новый пользователь не является суперпользователем.
    Статус ответа — `201`.
    """,
)
router.include_router(
    register_router,
    prefix='/auth',
    tags=['Аутентификация'],
)

users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
users_router.routes = [
    route for route in users_router.routes
    if getattr(route, 'name', None) != 'users:delete_user'
]
_document(
    users_router,
    'users:current_user',
    """
    Показать профиль текущего пользователя.

    Нужна авторизация. В ответе `id`, `email`, `is_active`,
    `is_superuser` и `is_verified`.
    """,
)
_document(
    users_router,
    'users:patch_current_user',
    """
    Изменить свой профиль.

    Нужна авторизация. Пользователь может сменить `email` и `password`.
    Поля `is_superuser`, `is_active` и `is_verified` так не меняются.
    """,
)
_document(
    users_router,
    'users:user',
    """
    Показать пользователя по идентификатору.

    Доступно только суперпользователю.
    Неизвестный `id` даёт статус `404`.
    """,
)
_document(
    users_router,
    'users:patch_user',
    """
    Изменить пользователя по идентификатору.

    Доступно только суперпользователю. Можно сменить почту, пароль,
    а также флаги `is_active`, `is_superuser` и `is_verified`.

    Удаление пользователя не предусмотрено: `DELETE` вернёт `405`.
    """,
)
router.include_router(
    users_router,
    prefix='/users',
    tags=['Пользователи'],
)
