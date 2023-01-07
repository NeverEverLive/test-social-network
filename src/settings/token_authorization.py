from pydantic import BaseSettings, Field


class TokenAuthorizationSettings(BaseSettings):
    token_ttl: int = Field(env="TOKEN_TTL", default=30)
    secret_key: str = Field(env="SECRET_KEY", default="")
    algorithms: str = Field(env="ALGORITHM", default="HS256")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
