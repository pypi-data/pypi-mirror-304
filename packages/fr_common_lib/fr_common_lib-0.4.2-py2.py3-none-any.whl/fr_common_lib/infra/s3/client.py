from contextlib import asynccontextmanager

from aiobotocore.session import AioSession
from . import S3Settings
from types_aiobotocore_s3 import S3Client

@asynccontextmanager
async def s3_client(session: AioSession, settings: S3Settings) -> S3Client:
        print('клиент s3 открываюсь')
        print(session)
        print(settings)
        config = {
            'aws_access_key_id': settings.ACCESS_KEY_ID,
            'aws_secret_access_key': settings.SECRET_ACCESS_KEY,
            'endpoint_url': settings.URL,
        }
        async with session.create_client(settings.SERVICE_NAME, **config) as client:
                yield client
        print('я клиент s3 закрываюсь')

        # print(context)
        # return client
        # await client.__aexit__(None, None, None)

