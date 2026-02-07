from contextlib import contextmanager

from app.core.config import settings
from app.models.tasks import Base
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

# create db engine
engine = create_engine(
    settings.DATABASE_URL,
    # pooling settings
    pool_pre_ping=True,
)

# create session factory (create db sessions)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def create_tables():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_session():
    db = SessionLocal()

    try:
        yield db
        db.commit()  # save changes if everythingwe nt well
    except Exception:
        db.rollback()  # undo changes if somthing went wrong
        raise
    finally:
        db.close()
