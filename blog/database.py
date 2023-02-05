from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQL_DB_URL = 'sqlite:///./blog.db'

engine = create_engine(SQL_DB_URL, connect_args={"check_same_thread": False})

sessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()