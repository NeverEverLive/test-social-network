from contextlib import asynccontextmanager
import aioredis

from src.settings import redis_settings

# @asynccontextmanager
async def get_session():
    host, port, database,  password = redis_settings.get_params()

    return await aioredis.from_url(f"redis://{host}:{port}/{database}", password=password)
