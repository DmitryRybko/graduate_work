"""Watching history API module."""

from logging import getLogger

from fastapi import APIRouter, Depends

from fastapi_paginate import Page, paginate

from models.history import WatchingHistory
from services.history import (
    WatchingHistoryService, get_watching_history_service
)


logger = getLogger(__name__)

router: APIRouter = APIRouter()


@router.get('/get/{user_id}', response_model=Page[WatchingHistory])
async def watching_history(
    user_id: str,
    srv: WatchingHistoryService = Depends(get_watching_history_service)
):
    """Return paginated watching history for a user."""
    logger.info(f'History for user: {user_id}')
    history: WatchingHistory = await srv.get_history_by_user_id(user_id)
    print(history, type(history))
    if not history:
        logger.error(f'History list for user {user_id} is empty.')
    return paginate(history)
