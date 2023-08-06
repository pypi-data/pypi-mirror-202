from typing import *
from typing import Union

import sqlalchemy.exc
from sqlalchemy.engine.url import URL
from sqlalchemy import text, MetaData, inspect
from sqlalchemy.schema import CreateSchema
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncConnection

_engine: Optional[AsyncEngine] = None
_is_started = False


async def create_db(engine_to_use, name: str):
    async with engine_to_use.connect() as conn:
        await conn.execute(text("COMMIT"))
        await conn.execute(text(f"CREATE DATABASE {name}"))


async def drop_db(engine_to_use, db_name: str):
    async with engine_to_use.connect() as conn:
        await conn.execute(text("COMMIT"))
        await conn.execute(text(f"DROP DATABASE IF EXISTS {db_name}"))


def create_test_database_url(url_to_modify: URL) -> URL:
    """
    Returns a modified URL where the database name is suffixed with _test
    :return:
    """
    return url_to_modify.set(database=url_to_modify.database + "_test")


async def schema_exists(conn: AsyncConnection, schema_name: str) -> bool:
    """
    Evaluates if a schema is present in the given database.

    Args:
        conn: AsyncConnection to work with.
        schema_name: Schema name to test

    Returns:
        bool
    """
    def inner(sync_conn):
        inspector = inspect(sync_conn)
        return inspector.dialect.has_schema(sync_conn, schema_name)

    return await conn.run_sync(inner)


async def init_async_test_db(db_url: URL, metadata: Union[list[MetaData], MetaData], drop_existing=False) -> AsyncEngine:
    """
    Connects to the configured database temporarily, issues CREATE commands to instantiate a test database,
    creates schemas if needed, disposes the engine and replaces the global engine with the test one.

    Args:
        db_url: Database URL
        metadata: Either a single MetaData object or a list of MetaData instances. If a list
            is passed, create commands will be issued for all objects in all MetaData instances.
        drop_existing: If set to True, it will DROP the database first.

    Returns:
        Reference to the instantiated test engine.
    """
    global _engine
    global _is_started

    temp_engine = create_async_engine(db_url)
    test_db_url = create_test_database_url(db_url)

    if _is_started is False:

        if drop_existing is True:
            await drop_db(temp_engine, test_db_url.database)

        await create_db(temp_engine, test_db_url.database)

        _engine = create_async_engine(test_db_url)

        async with _engine.begin() as conn:
            if isinstance(metadata, MetaData):
                metadata = [metadata]
            for metadata_ in metadata:
                if not await schema_exists(conn, metadata_.schema):
                    await conn.execute(
                        CreateSchema(metadata_.schema)
                    )

                await conn.run_sync(metadata_.create_all)

        _is_started = True

    return _engine


async def destroy_async_test_db(db_url):
    """
    If the module's engine is a test engine, it will dispose it.
    Then, connects to the given db_url as "main" database and drops the test database.

    :param db_url:
    :return:
    """
    global _engine
    global _is_started

    if _is_started is True:
        await _engine.dispose()
        _engine.sync_engine.pool.dispose()

        temp_engine = create_async_engine(db_url)
        test_db_url = create_test_database_url(db_url)

        await drop_db(temp_engine, test_db_url.database)
        _is_started = False

    return
