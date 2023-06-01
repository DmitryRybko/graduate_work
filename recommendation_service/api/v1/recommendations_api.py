from dotenv import load_dotenv
from fastapi import APIRouter, Response, Request
from starlette import status
from loguru import logger

from api.v1.schemas import RecommendationsResponse

# since relative imports work from file that is run,
# IDE will show error here but its not
from config import settings
from services.jwt_decode import decode_jwt
from utils.get_recom_from_redis import retrieve_recom_movies

logger.add("debug.log", level=settings.log_level)

router = APIRouter()


@router.get("/", response_model=RecommendationsResponse)
def get_recommendations(request: Request, response: Response) -> RecommendationsResponse:
    # в составе JWT токена приезжает user_id (email), который мы декодируем и используем для запроса в database
    try:
        token: str = request.headers["Authorization"]
        user_email: str | None = decode_jwt(token)
        logger.info(f"{user_email}")
    except KeyError:
        user_email = None
        logger.info(f"user not logged in")

    movies_recom = retrieve_recom_movies(user_email)
    logger.debug(movies_recom)
    return RecommendationsResponse(movies_data=movies_recom)
