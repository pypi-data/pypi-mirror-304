from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class RedisConfig(BaseSettings):

    HOST: str
    IN_PORT: int

    @property
    def URL(self):
        return f'redis://{self.HOST}:{self.IN_PORT}'

    model_config = ConfigDict(
        case_sensitive = True,
        env_prefix = 'RS_'
    )


