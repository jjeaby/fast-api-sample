from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from common.Log import Log
from common.config import Config


class Connect:
    """
    SQLAlchemy Database Connection Setting
    """

    def __init__(self, app: FastAPI = None, **kwargs):
        self._engine = None
        self._logger = Log.__logger__
        if app is not None:
            self.__init_database(app=app, **kwargs)

    def __init_database(self, app: FastAPI, **kwargs):
        """
        Database Connection
        """
        config = Config.dict()
        self._engine = create_engine(
            f"postgresql://{config['USER']}"
            f":{config['PASSWORD']}"
            f"@{config['HOST']}"
            f":{config['PORT']}"
            f"/{config['DATABASE']}",
            pool_size=int(config['POOL_SIZE']),
            max_overflow=int(config['MAX_OVERFLOW'])
        )

        @app.on_event("startup")
        async def startup():
            app.state.engine = self._engine
            self._logger.info("DB connected.")

        @app.on_event("shutdown")
        async def shutdown():
            app.state.session.close()
            self._logger.info("DB disconnected")


Base = declarative_base()
database = Connect()
