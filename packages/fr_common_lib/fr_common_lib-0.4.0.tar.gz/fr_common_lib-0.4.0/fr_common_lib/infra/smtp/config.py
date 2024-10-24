from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class SmtpConfig(BaseSettings):

    HOST: str
    PORT: int
    EMAIL: str
    PASSWORD: str

    model_config = ConfigDict(
        case_sensitive=True,
        env_prefix='SM_'
    )
