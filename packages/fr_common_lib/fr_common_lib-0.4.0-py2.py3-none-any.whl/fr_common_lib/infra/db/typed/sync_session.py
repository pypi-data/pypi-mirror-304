from contextlib import contextmanager
from typing import Callable, ContextManager

from attrs import define
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker


@define
class SyncSessionManager:

    _engine: Engine
    _session_factory: sessionmaker[Session]

    @contextmanager
    def __call__(self, schema: str, **kwargs) -> ContextManager[Session]:

        connectable = self._engine.execution_options(schema_translate_map=dict(tenant=schema))
        session = self._session_factory(bind=connectable, **kwargs)

        try:
            yield session
            session.commit()
        except Exception as exc:
            session.rollback()
            raise
        finally:
            session.close()
