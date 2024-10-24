from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class UrlTokenConfig(BaseSettings):

    SECRET_KEY: str
    SALT: str

    model_config = ConfigDict(
        case_sensitive = True,
        env_prefix = 'ID_'
    )

