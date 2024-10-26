from dishka import Provider, provide, Scope
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session

from fr_common_lib.infra.db.typed.async_session import DbSessManager
from fr_common_lib.infra.db.typed.config import DbConfig


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

    session_manager = provide(DbSessManager, scope=Scope.APP)
