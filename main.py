import argparse
import logging
import os
from configparser import ConfigParser
from datetime import date
from os.path import dirname
from typing import Optional

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse

from util.log import config_logging

app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


@app.get("/",
         name="Rest Api For Health Check",
         description="Rest Api 가 살아 있는지 확인 하는 Rest Api"
         )
def root():
    return {"Hello": "Fast-Jin"}


@app.get("/web",
         name="Rest Api For index.html",
         description="index.html 을 브라우저에 보여주는 주는 Rest Api"
         )
async def web():
    file_name = "index.html"
    file_path = os.path.join(dirname(__file__), 'static', file_name)
    return FileResponse(path=file_path, media_type='text/html')


@app.get('/favicon.ico',
         name="Rest Api For favicon.ico",
         description="favicon.ico 을 브라우저에 보여주는 주는 Rest Api"
         )
async def favicon():
    file_name = "favicon.ico"
    file_path = os.path.join(dirname(__file__), 'static/favicon.ico')
    return FileResponse(path=file_path, headers={"Content-Disposition": "attachment; filename=" + file_name})


# A Pydantic modelE : Request
class TestReq(BaseModel):
    id: Optional[int] = Field(None, title='id 값')
    name: str = Field(None, title='name 값')
    joined: date = Field(title='날짜')


# A Pydantic model : Response
class TestRes(BaseModel):
    status_code: int = Field(title='return status code ')
    status_message: str = Field(title='return status message ')


@app.post('/test',
          name="Rest Api For test",
          description="fast-api get 테스트를 위한 Rest Api",
          response_model=TestRes
          )
def test(testReq: TestReq):
    request_json = dict(testReq)
    logging.debug('request_json : %s', request_json)
    result = {'status_code': 200, 'status_message': "success"}

    testRes = TestRes(**result)
    return JSONResponse(testRes.dict())


if __name__ == '__main__':
    config = ConfigParser()
    config.read('config/config.ini')

    logging = config_logging(logging.DEBUG)

    parser = argparse.ArgumentParser(description='Run Fast-Jin Server')
    parser.add_argument('--mode', type=str, required=False, default='dev', choices=['dev', 'prd'],
                        help='run mode.(ex. dev, prod). default value is a dev')

    args = parser.parse_args()
    run_mode = str(args.mode)

    logging.info("===================================================")
    logging.info('Fast-Jin SERVER RUN MODE [%s]', run_mode)
    logging.info('Fast-Jin SERVER RUN PORT [%s]', config[run_mode.upper()]['port'])
    logging.info("===================================================")

    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="debug", reload=False, reload_dirs=['./'],
                debug=True)
