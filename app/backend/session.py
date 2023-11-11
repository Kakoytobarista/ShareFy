import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

current_directory = os.path.abspath(os.path.dirname(""))
path_to_db_folder = os.path.abspath(os.path.join(current_directory, ".."))
db_path = os.path.join(path_to_db_folder, 'mydatabase.db')


DATABASE_URL = f"sqlite+aiosqlite:///{db_path}"

engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
