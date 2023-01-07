from pydantic import BaseSettings, Field


class PostgresSettings(BaseSettings):
    user: str = Field(env="POSTGRES_USER", default="postgres")
    password: str = Field(env="POSTGRES_PASSWORD", default="postgres")
    host: str = Field(env="POSTGRES_HOST", default="localhost")
    port: int = Field(env="POSTGRES_PORT", default=5432)
    database: str = Field(env="POSTGRES_DATABASE", default="postgres")

    def get_url(self):
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"