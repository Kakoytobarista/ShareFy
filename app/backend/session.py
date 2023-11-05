import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

current_directory = os.path.abspath(os.path.dirname(""))
path_to_db_folder = os.path.abspath(os.path.join(current_directory, ".."))
db_path = os.path.join(path_to_db_folder, 'mydatabase.db')


DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# class DbSession:
#
#     async def __call__(self):
#         db_session = SessionLocal()
#         try:
#             yield db_session
#         finally:
#             db_session.close()
#

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
