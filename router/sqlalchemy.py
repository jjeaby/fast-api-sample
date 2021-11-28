from contextlib import closing

from fastapi import APIRouter, Request

from common.config import Config
from common.database.Model import Links
from common.database.Session import database_session

router = APIRouter()

"""
SQLAlchemy Example - session and connection pool
"""


@router.get("/session/{id}")
async def scope_session(id: int):
    with database_session(Config.dict()) as session:
        response_result = {}
        result = (
            session.query(Links)
                .filter(Links.id == id)
                .one_or_none()
        )
        if result:
            response_result = result.to_dict()
    return {id: response_result}


@router.get("/pool/{text}")
async def connection_pool(request: Request, text: str):
    with closing(request.app.state.engine.connect()) as conn:
        result = conn.execute(f"SELECT 'FAST API SAMPLE DB Connect - {text}'").fetchone()
    return {'TEXT': result[0]}
