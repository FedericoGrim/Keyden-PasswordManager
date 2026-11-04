from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
import os
import logging
from dotenv import load_dotenv

from infrastructure.exceptions.database_exception import PostgreSqlConnectionException
from collections.abc import Generator
from typing import Any

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_engine(
    DATABASE_URL,
    isolation_level="SERIALIZABLE",
    pool_size=10,
    max_overflow=5,
    pool_timeout=30,
    pool_recycle=1800,
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db() -> Generator[Session, Any, None]:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except PostgreSqlConnectionException as e:
        logging.error(f"Database connection error: {e}")
        db.rollback()
        raise
    except Exception as e:
        logging.error(f"Database error: {e}")
        db.rollback()
        raise  # rilancia l'eccezione originale
    finally:
        db.close()
