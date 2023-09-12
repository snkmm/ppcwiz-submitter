from contextlib import contextmanager

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from crawler import settings

Base = declarative_base()
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
    pool_pre_ping=True
)
Session = sessionmaker(bind=engine)
#Session = sessionmaker(bind=engine, autoflush=False)

@contextmanager
def session_scope() -> Session:
    session = Session()
    #session.autoflush = False
    try:
        yield session
        session.commit()
    except Exception as e:
        logger.error(f'Database Error: {e}')
        #session.rollback()
        raise e
    finally:
        session.close()
