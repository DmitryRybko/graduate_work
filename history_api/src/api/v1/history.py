"""Watching history API module."""

from loguru import logger

from fastapi import APIRouter, Depends

from fastapi_paginate import Page, paginate

from models.history import WatchingHistory
from services.history import (
    WatchingHistoryService, get_watching_history_service
)

router: APIRouter = APIRouter()


# @router.get('/get/{user_id}', response_model=Page[WatchingHistory])
# def watching_history(
#     user_id: str,
#     srv: WatchingHistoryService = Depends(get_watching_history_service)
# ):
#     """Return paginated watching history for a user."""
#     logger.info(f'History for user: {user_id}')
#     history: WatchingHistory = srv.get_history_by_user_id(user_id)
#     if not history:
#         logger.error(f'History list for user {user_id} is empty.')
#     return history


@router.get('/get/{user_id}')
def watching_history(user_id: str):
    """Return paginated watching history for a user."""
    logger.info(f'History for user: {user_id}')
    history = {user_id: ["81fb27b5-9851-44db-bb31-80a73427dec1",
                         "e85f69b6-28de-4e67-8c38-cb6ab1fe1f4a",
                         "5e4b16bb-ab14-4be0-a0d0-c9206b6799ee",
                         "3cca703f-722d-4c16-acd0-97d8e6cbf342",
                         "306dbc98-934c-4612-a125-a7824231cc3e"], }
    if not history:
        logger.error(f'History list for user {user_id} is empty.')
    return history
