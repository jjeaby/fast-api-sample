import argparse
import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from common.Log import Log
from common.config import Config
from common.database.Connect import Connect
from router import sqlalchemy, web, root, method

logger = Log.__logger__
config = Config.dict()


def create_app(title, description):
    """
    FastAPI Instance Create and Setting
    :param title: App title
    :param description: App Description
    :return: FastAPI Instance
    """

    parser = argparse.ArgumentParser(description='Run Jin\'s FastAPI Server')
    parser.add_argument('--run_mode', type=str, required=True, choices=['local', 'dev', 'prd'],
                        help='run mode.(ex. local, dev, prod). default value is a dev')
    args = parser.parse_args()
    os.environ["RUN_MODE"] = str(args.run_mode).upper()
    backend_cors_origins = [
        "http://localhost",
        "http://localhost:8080",
    ]

    fast_api = FastAPI(title=title, description=description)
    fast_api.add_middleware(
        CORSMiddleware,
        allow_origins=backend_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    fast_api.mount("/static", StaticFiles(directory="static", html=True), name="static")
    Connect(fast_api)

    fast_api.include_router(root.router, tags=["root"])
    fast_api.include_router(sqlalchemy.router, tags=["SQLAlchemy"])
    fast_api.include_router(web.router, tags=["web"])

    fast_api.include_router(
        root.router,
        tags=["ROOT - GET"],
    )
    fast_api.include_router(
        sqlalchemy.router,
        tags=["SQLAlchemy - Session/Connection Pool"],
    )
    fast_api.include_router(
        method.router,
        tags=["METHOD - GET/POST"],
    )
    fast_api.include_router(
        web.router,
        tags=["WEB - index.html, favicon"],
    )
    return fast_api


app = create_app('Jin\'s FastAPI Server', 'This is Jin\'s FastAPI Swagger Document')

if __name__ == "__main__":
    """
    Running uvicorn and show running Information
    """
    logger.info("===================================================")
    logger.info('Jin\'s SERVER RUN MODE [%s]', config['run_mode'].upper())
    logger.info('Jin\'s SERVER RUN PORT [%s]', config['run_port'])
    logger.info("===================================================")
    reload = True
    if config['run_mode'].upper() == 'PRD':
        reload = False
    uvicorn.run("main:app",
                host="0.0.0.0",
                port=int(config['run_port']),
                log_level="debug",
                reload=reload,
                reload_dirs=['./'],
                debug=True,
                workers=4)
