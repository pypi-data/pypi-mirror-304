from collections.abc import AsyncIterator

from dishka import provide, Scope, Provider
from aiosmtplib import SMTP
from .config import SmtpConfig


class SmtpProv(Provider):


    @provide(scope=Scope.APP)
    def config(self) -> SmtpConfig:
        return SmtpConfig()

    @provide(scope=Scope.APP)
    async def client(self, settings: SmtpConfig) -> AsyncIterator[SMTP]:
        async with SMTP(
            hostname=settings.HOST,
            port=settings.PORT,
            validate_certs=True,
            use_tls=True
        ) as client:
            await client.login(settings.EMAIL, settings.PASSWORD)
            client.default_sender = settings.EMAIL
            yield client



