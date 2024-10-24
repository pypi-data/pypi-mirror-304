
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict


class JwtConfig(BaseSettings):

    SECRET_KEY: str
    ALG: str
    ACCESS_EXP: int = Field(..., description="Access token expiration time in minutes")
    REFRESH_EXP: int = Field(..., description="Refresh token expiration time in minutes")

    model_config = ConfigDict(
        case_sensitive = True,
        env_prefix = 'JT_'
    )

