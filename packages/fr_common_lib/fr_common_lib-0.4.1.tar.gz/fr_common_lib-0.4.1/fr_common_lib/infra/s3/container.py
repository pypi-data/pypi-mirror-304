from aiobotocore.session import get_session, AioSession
from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Provider
from types_aiobotocore_s3.client import S3Client

from . import S3Manager, S3Settings, s3_client


class S3Cntr(DeclarativeContainer):

    settings: Provider[S3Settings] = providers.Singleton(S3Settings)

    session: Provider[AioSession] = providers.Singleton(get_session)

    client: Provider[S3Client] = providers.Resource(
        s3_client,
        session=session,
        settings=settings,
    )

    manager: Provider[S3Manager] = providers.Singleton(
        S3Manager,
        client=client.provided,
        default_bucket=settings.provided.DEFAULT_BUCKET,
    )

