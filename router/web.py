import os
from os.path import dirname

from fastapi import APIRouter
from fastapi.responses import FileResponse

from common.util import root_path

router = APIRouter()
"""
Front-End Serving Sample
"""

@router.get('/favicon.ico')
async def favicon():
    file_name = "favicon.ico"
    file_path = os.path.join(root_path(), 'static/favicon.ico')
    return FileResponse(path=file_path, headers={"Content-Disposition": "attachment; filename=" + file_name})


@router.get("/web")
async def web():
    file_name = "index.html"
    file_path = os.path.join(root_path(), 'static', file_name)
    return FileResponse(path=file_path, media_type='text/html')
