from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from common.Log import Log

Base = declarative_base()


def _configure_database(config):
    """
    SQLAlchemy database session maker
    :param config:
    :return: session
    """
    engine = create_engine(
        f"postgresql://{config['USER']}"
        f":{config['PASSWORD']}"
        f"@{config['HOST']}"
        f":{config['PORT']}"
        f"/{config['DATABASE']}")

    return sessionmaker(bind=engine)


@contextmanager
def database_session(config):
    """Provide a SQLAlchemy's db session scope."""
    try:
        logger = Log.__logger__
        db_session = _configure_database(config)
        session = db_session()
        yield session
        session.commit()
    except SQLAlchemyError as error:
        session.rollback()
        logger.warning(
            "Failed to communicate with Database : %s", error, exc_info=True
        )
    finally:
        session.close()
