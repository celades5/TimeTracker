from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# DATABASE_URL =  "db_type://db_user:password@host:port/db_name"
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/TimeTracker"

                                    # allowing multiple threads to share db connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()