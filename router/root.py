from fastapi import APIRouter

router = APIRouter()

"""
Hana Database Example by  hdbcli
"""


@router.get("/")
async def root():
    return {"Hello": "Jin\'s FastAPI Server"}
