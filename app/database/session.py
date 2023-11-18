import os
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from models.v1.user import Base

load_dotenv()

current_directory = os.path.abspath(os.path.dirname(""))
path_to_db_folder = os.path.abspath(os.path.join(current_directory, ".."))
db_path = os.path.join(path_to_db_folder, "mydatabase.db")

db_username = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DATABASE")


test_environment = os.getenv("TEST_ENVIRONMENT", 1)
DATABASE_URL = f"postgresql+asyncpg://{db_username}:{db_password}@db/{db_name}"
# DATABASE_URL = f"sqlite+aiosqlite:///{db_path}"

engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
