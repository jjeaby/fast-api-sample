import argparse
import logging
import os
from configparser import ConfigParser
from os.path import dirname

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from util.log import config_logging


app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")



@app.get("/")
def read_root():
    return {"Hello": "Fast-Jin"}


@app.get("/web")
async def web():
    file_name = "index.html"
    file_path = os.path.join(dirname(__file__), 'static', file_name)
    return FileResponse(path=file_path, media_type='text/html')


@app.get('/favicon.ico')
async def favicon():
    file_name = "favicon.ico"
    file_path = os.path.join(dirname(__file__), 'static/favicon.ico')
    return FileResponse(path=file_path, headers={"Content-Disposition": "attachment; filename=" + file_name})


@app.get('/abc')
def abc_test():
    return {'hello': 'abc-test'}


if __name__ == "__main__":
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
