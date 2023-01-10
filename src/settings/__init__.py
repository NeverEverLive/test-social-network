from src.settings.postgres_settings import PostgresSettings
from src.settings.async_postgres_settings import AsyncPostgresSettings
from src.settings.token_authorization import TokenAuthorizationSettings
from src.settings.redis_settings import RedisSettings


postgres_settings = PostgresSettings()
async_postgres_settings = AsyncPostgresSettings()
token_authorization = TokenAuthorizationSettings()
redis_settings = RedisSettings()
