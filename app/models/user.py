from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):

    def __repr__(self):
        return (
            f'{type(self).__name__}('
            f'id={self.id}, email={self.email!r}, '
            f'is_active={self.is_active}, '
            f'is_superuser={self.is_superuser})'
        )
