#!/usr/bin/env python3
"""Main module of watching history api."""

from logging import getLogger

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from fastapi_paginate import add_pagination

import uvicorn

from api.v1 import history
from core.config import config


logger = getLogger(__name__)


app = FastAPI(
    title=config.title,
    default_response_class=ORJSONResponse
)

add_pagination(app)

app.include_router(history.router, prefix='/api/v1/history', tags=['history'])


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=int(config.port_to_run),
    )
