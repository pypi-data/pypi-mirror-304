from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession, async_sessionmaker

from ..typed import DbConfig, AsyncSessionManager


class DbAsyncProv(Provider):


    @provide(scope=Scope.APP)
    def config(self) -> DbConfig:
        return DbConfig()

    @provide(scope=Scope.APP)
    def engine(self, settings: DbConfig) -> AsyncEngine:
        return create_async_engine(
            settings.ASYNC_URI,
            echo=settings.ECHO,
            future=True,
            pool_size=settings.POOL_SIZE,
            max_overflow=settings.MAX_OVERFLOW,
        )

    @provide(scope=Scope.APP)
    def session_factory(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind = engine, class_ = AsyncSession)

    session_manager = provide(AsyncSessionManager, scope=Scope.APP)



