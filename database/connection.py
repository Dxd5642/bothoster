from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from settings.setting import DATABASE_URL, DEBUG

if not DATABASE_URL:
    raise ValueError("DATABASE_URL не задан в .env")


engine = create_async_engine(
    DATABASE_URL,
    echo=False
)

async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    async with async_session_maker() as session:
        yield session

