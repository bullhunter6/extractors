"""Database configuration and session management."""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import create_engine, event
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from typing import AsyncGenerator
from contextlib import contextmanager

from server.core.config import get_settings

settings = get_settings()

# SQLite connection args for better concurrency
sqlite_connect_args = {
    "check_same_thread": False,
    "timeout": 30,  # Wait up to 30 seconds for locks
}

# Check if using SQLite
is_sqlite = "sqlite" in settings.DATABASE_URL

# Create async engine - SQLite uses StaticPool for better thread sharing
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,  # Reduce noise
    future=True,
    connect_args=sqlite_connect_args if is_sqlite else {},
    # SQLite with aiosqlite uses NullPool by default, so no pool settings
)

# Create sync engine for Celery workers
sync_db_url = settings.DATABASE_URL.replace("+aiosqlite", "")
sync_engine = create_engine(
    sync_db_url,
    echo=False,
    connect_args=sqlite_connect_args if is_sqlite else {},
    # Use StaticPool for SQLite to share connections across threads
    poolclass=StaticPool if is_sqlite else None,
)


# Enable WAL mode for SQLite (better concurrent access)
@event.listens_for(engine.sync_engine, "connect")
def set_sqlite_pragma_async(dbapi_connection, connection_record):
    """Set SQLite pragmas for better concurrency (async engine)."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA busy_timeout=30000")  # 30 second timeout
    cursor.execute("PRAGMA cache_size=-64000")  # 64MB cache
    cursor.close()


@event.listens_for(sync_engine, "connect")
def set_sqlite_pragma_sync(dbapi_connection, connection_record):
    """Set SQLite pragmas for better concurrency (sync engine)."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA busy_timeout=30000")  # 30 second timeout
    cursor.execute("PRAGMA cache_size=-64000")  # 64MB cache
    cursor.close()

# Create async session factory (for FastAPI)
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Create sync session factory (for Celery workers)
SyncSessionLocal = sessionmaker(
    sync_engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Base class for models
Base = declarative_base()


@contextmanager
def get_sync_db():
    """
    Context manager for sync database session (for Celery workers).
    
    Yields:
        Session: Database session
    """
    session = SyncSessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for database session.
    
    Yields:
        AsyncSession: Database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """Initialize database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Close database connections."""
    await engine.dispose()
