from pydantic import BaseSettings, Field
from dotenv import load_dotenv


load_dotenv()


class RedisSettings(BaseSettings):
    host: str = Field(env="REDIS_HOST", default="localhost")
    port: str = Field(env="REDIS_PORT", default=6379)
    database: str = Field(env="REDIS_DB", default=0)
    password: str = Field(env="REDIS_PASSWORD")

    def get_params(self):
        return self.host, self.port, self.database, self.password
