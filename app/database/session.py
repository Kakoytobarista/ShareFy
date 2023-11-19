import os
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from logger import logger
from models.v1.user import Base

load_dotenv()

current_directory = os.path.abspath(os.path.dirname(""))
path_to_db_folder = os.path.abspath(os.path.join(current_directory, ".."))
db_path = os.path.join(path_to_db_folder, "mydatabase.db")

db_username = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DATABASE")


test_environment = int(os.getenv("TEST_ENVIRONMENT")) == 1
if test_environment:
    DATABASE_URL = f"sqlite+aiosqlite:///{db_path}"
    logger.debug(f"In test env and use {DATABASE_URL}")
else:
    DATABASE_URL = f"postgresql+asyncpg://{db_username}:{db_password}@db/{db_name}"
    logger.debug(f"In prod env and use {DATABASE_URL}")

engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    db = SessionLocal()
    yield db
