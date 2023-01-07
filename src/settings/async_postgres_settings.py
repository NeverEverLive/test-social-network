from pydantic import BaseSettings, Field


class AsyncPostgresSettings(BaseSettings):
    user = Field(env="POSTGRES_USER", default="postgres")
    password = Field(env="POSTGRES_PASSWORD", default="postgres")
    host = Field(env="POSTGRES_HOST", default="localhost")
    port = Field(env="POSTGRES_PORT", default=5432)
    database = Field(env="POSTGRES_DATABASE", default="postgres")

    def get_url(self):
        return f"postgresql+asyncpg://{self.host}:{self.port}@{self.user}:{self.password}/{self.database}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
