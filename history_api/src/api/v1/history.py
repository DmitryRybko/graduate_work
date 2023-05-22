"""Watching history API module."""

from logging import getLogger

from fastapi import APIRouter, Depends

from fastapi_paginate import Page, paginate

from models.history import WatchingHistory
from services.history import get_history


logger = getLogger(__name__)

router: APIRouter = APIRouter()


@router.get('/history/', response_model=Page[WatchingHistory])
def watching_history(user_id: str):
    """Return paginated watching history for a user."""
    logger.info(f'History for user: {user_id}')
    history: WatchingHistory = get_history(user_id)
    if not history:
        logger.error(f'History list for user {user_id} is empty.')
    return paginate(history)
