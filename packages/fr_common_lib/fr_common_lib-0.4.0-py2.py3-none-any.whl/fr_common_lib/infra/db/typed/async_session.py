from contextlib import asynccontextmanager
from typing import AsyncContextManager

from attr import define
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession


@define
class AsyncSessionManager:

    _engine: AsyncEngine
    _session_factory: async_sessionmaker[AsyncSession]

    @asynccontextmanager
    async def __call__(self, schema: str, **kwargs) -> AsyncContextManager[AsyncSession]:

        connectable = self._engine.execution_options(schema_translate_map=dict(tenant=schema))
        session = self._session_factory(bind=connectable, **kwargs)

        try:
            yield session
            await session.commit()
        except Exception as exc:
            await session.rollback()
            raise
        finally:
            await session.close()

