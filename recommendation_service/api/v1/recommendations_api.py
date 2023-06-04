import sys

from fastapi import APIRouter, Request, Depends
from loguru import logger

from recommendation_service.api.v1.schemas import RecommendationsResponse
from recommendation_service.config import settings
from recommendation_service.services.jwt_decode import ParseJWTToken
from recommendation_service.utils.get_recom_from_redis import retrieve_recom_movies

logger.add(sys.stdout, level=settings.log_level)

router = APIRouter()


@router.get("/", response_model=RecommendationsResponse)
def get_recommendations(request: Request, token_parser=Depends(ParseJWTToken)) -> RecommendationsResponse:
    # в составе JWT токена приезжает user_id (email), который мы декодируем и используем для запроса в database
    try:
        token: str = request.headers["Authorization"]
        user_email: str | None = token_parser(token)
        logger.info(f"{user_email}")
    except KeyError:
        user_email = None
        logger.info(f"user not logged in")
        user_email = "default_user"
    movies_recom = retrieve_recom_movies(user_email)
    logger.debug(movies_recom)
    return RecommendationsResponse(movies_data=movies_recom)
