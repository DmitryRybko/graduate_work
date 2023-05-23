"""Conftest module."""

import os
from typing import AsyncGenerator

from asgi_lifespan import LifespanManager

from motor.motor_asyncio import AsyncIOMotorClient

from fastapi import FastAPI

from httpx import AsyncClient

import pytest

import pytest_asyncio


@pytest.fixture
def app() -> FastAPI:
    """Fixture to return fastapi app."""
    from ..src.main import app
    return app


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncGenerator:
    """Return test fastapi client."""
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url='http://testserver',
            headers={'Content-Type': 'application/json'}
        ) as client:
            yield client


@pytest_asyncio.fixture
async def mongo_db(scope='session') -> AsyncIOMotorClient:
    """Return mongo db client for tests."""
    url = os.environ.get('mongo_db_url')
    db_name = os.environ.get('mongo_db_db_name')
    yield AsyncIOMotorClient(url)[db_name]
