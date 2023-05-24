from dotenv import load_dotenv
from fastapi import APIRouter, Response, Request
from starlette import status
from loguru import logger

from api.v1.schemas import RecommendationsResponse

# since relative imports work from file that is run,
# IDE will show error here but its not
from config import settings
from services.jwt_decode import decode_jwt

# load_dotenv здесь нужен несмотря на наличие pydantic (при запуске не из docker),
# так как pydantic не умеет искать env в parent директориях
load_dotenv()

router = APIRouter()


@router.get("/", response_model=RecommendationsResponse)
def get_recommendations(request: Request, response: Response):
    # в составе JWT токена приезжает user_id (email), который мы декодируем и используем для запроса в database
    try:
        token = request.headers["Authorization"]
        user_email = decode_jwt(token)
        logger.info(f"{user_email}")
        return RecommendationsResponse(key="key", value="value")
    except KeyError:
        user_email = None
        logger.info(f"user not logged in")
        return RecommendationsResponse(key="key", value="user not logged in")
        # brokers: list = settings.kafka_brokers

