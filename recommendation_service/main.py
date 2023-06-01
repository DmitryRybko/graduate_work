"""Main recomendation service module."""

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis import asyncio as aioredis

import uvicorn

from api.v1 import recommendations_api
from config import settings
from db import redis

app = FastAPI(
    title=settings.project_name,
    docs_url='/api_recommendations/openapi',
    openapi_url='/api_recommendations/openapi.json',
    # Changing default JSON serializer to optimized version.
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    """Magic method to run something when server is starting.

    It connects to redis and elasticsearch in event-loop.
    """
    redis.redis = aioredis.from_url(
        f'redis://{settings.redis_host}:{settings.redis_port}',
        encoding='utf8',
        decode_responses=True
    )


@app.on_event('shutdown')
async def shutdown():
    """Magic method to run something when server is shutting down.

    It closes connections with databases during shutdown.
    """
    await redis.redis.close()


app.include_router(
    recommendations_api.router,
    prefix='/api/v1/recommendations',
    tags=['recommendations']
)

if __name__ == '__main__':
    # The app can also be run by
    # `uvicorn main:app --host 0.0.0.0 --port 8003` cmd.
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8003,
    )
