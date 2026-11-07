from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = 'Благотворительный фонд поддержки котиков QRKot'
    app_description: str = (
        'Сервис фонда QRKot: целевые сборы на помощь котикам '
        'и автоматическое распределение пожертвований.'
    )
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


settings = Settings()
