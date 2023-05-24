#!/usr/bin/env python3
"""Main module of watching history api."""

from logging import getLogger

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from fastapi_paginate import add_pagination

import uvicorn

from api.v1 import history
from core.config import config
from db import db, mongo_db


logger = getLogger(__name__)


app = FastAPI(
    title=config.title,
    default_response_class=ORJSONResponse
)


@app.on_event('startup')
async def startup() -> None:
    """Magic method to run something when server is starting."""
    db.db = mongo_db.MondoDB(
        config.mongo_db_url,
        config.mongo_db_db_name,
        config.mongo_db_collection_name
    )

app.include_router(history.router, prefix='/api/v1/history', tags=['history'])

add_pagination(app)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=int(config.port_to_run),
    )
