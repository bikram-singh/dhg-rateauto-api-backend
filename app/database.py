from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.engine.url import URL

from app.config import settings

engine = None
AsyncSessionLocal = None


class Base(DeclarativeBase):
    pass


async def init_db():
    global engine, AsyncSessionLocal

    # Import all models so SQLAlchemy registers them before create_all
    import app.models.department  # noqa: F401
    import app.models.hospital    # noqa: F401
    import app.models.vaccine     # noqa: F401
    import app.models.pricing     # noqa: F401

    db_url = URL.create(
        drivername="postgresql+asyncpg",
        username=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
    )

    engine = create_async_engine(
        db_url,
        echo=False,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )
    AsyncSessionLocal = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)


async def close_db():
    if engine:
        await engine.dispose()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session