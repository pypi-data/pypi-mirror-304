from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class S3Settings(BaseSettings):

    SERVICE_NAME: str
    HOST: str
    ACCESS_KEY_ID: str
    SECRET_ACCESS_KEY: str
    DEFAULT_BUCKET: str
    DEFAULT_BUCKET_HOST: str

    @property
    def URL(self):
        return f'https://{self.HOST}'

    model_config = ConfigDict(
        case_sensitive = True,
        env_prefix = 'S3_'
    )



