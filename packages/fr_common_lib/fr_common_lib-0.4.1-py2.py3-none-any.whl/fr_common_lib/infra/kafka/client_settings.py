import os

from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    SERVICE_NAME: str
    HOST: str
    IN_PORT: int

    model_config = ConfigDict(
        case_sensitive = True,
        env_prefix = os.getenv('KF_CLIENT_PREFIX')
    )


settings = Settings()
