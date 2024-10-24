from dishka import Provider, provide, Scope
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session
from ..typed import SyncSessionManager, DbConfig


class DbSyncProv(Provider):

    config = provide(DbConfig, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def engine(self, settings: DbConfig) -> Engine:
        return create_engine(
            settings.SYNC_URI,
            echo=settings.ECHO,
            future=True,
            pool_size=settings.POOL_SIZE,
            max_overflow=settings.MAX_OVERFLOW,
        )

    @provide(scope=Scope.APP)
    def session_factory(self, engine: Engine) -> sessionmaker[Session]:
        return sessionmaker(bind=engine)

    session_manager = provide(SyncSessionManager, scope=Scope.APP)
