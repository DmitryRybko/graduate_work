"""Watching history API module."""

# Default libs
from uuid import UUID

# Third party libs
from fastapi import APIRouter, Depends

from loguru import logger

# Project imports
from models.history import WatchingHistory

from services.history import (
    WatchingHistoryService, get_watching_history_service
)

router: APIRouter = APIRouter()


@router.get('/get/{user_id}', response_model=dict)
async def watching_history(
    user_id: UUID,
    limit: int = 1000,
    srv: WatchingHistoryService = Depends(get_watching_history_service)
):
    """Return paginated watching history for a user."""
    logger.info(f'History for user: {user_id}')
    history: list[WatchingHistory] = await srv.get_history_by_user_id(
        str(user_id), limit
    )
    if not history:
        logger.error(f'History list for user {user_id} is empty.')
    watched_films: list = [h.film_id for h in history]
    return {history[0].user_id: watched_films}


@router.post('/add/', response_model=dict)
async def add_watched_film(
    watching_history: WatchingHistory,
    srv: WatchingHistoryService = Depends(get_watching_history_service)
) -> dict:
    """Add watched film."""
    result: None | str = srv.add_watched_film(
        watching_history.user_id, watching_history.film_id
    )
    if result is None:
        return {'success': 'OK'}
    else:
        return {'error': result}


@router.get('/is-watched', response_model=dict)
async def film_is_watched(
    watched_film: WatchingHistory,
    srv: WatchingHistoryService = Depends(get_watching_history_service)
) -> dict:
    """Return True if the user is watched the film."""
    result: bool | str = srv.is_watched(
        watched_film.user_id, watched_film.film_id
    )
    if type(result) == bool:
        return {'is_watched': result}
    else:
        return {'error': result}


# TODO Del this block when the debug is completed.
# @router.get('/get/{user_id}')
# def watching_history(user_id: str):
#     """Return paginated watching history for a user."""
#     logger.info(f'History for user: {user_id}')
#     history = {user_id: ["81fb27b5-9851-44db-bb31-80a73427dec1",
#                          "e85f69b6-28de-4e67-8c38-cb6ab1fe1f4a",
#                          "5e4b16bb-ab14-4be0-a0d0-c9206b6799ee",
#                          "3cca703f-722d-4c16-acd0-97d8e6cbf342",
#                          "306dbc98-934c-4612-a125-a7824231cc3e"], }
#     if not history:
#         logger.error(f'History list for user {user_id} is empty.')
#     return history
