from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from recommendation_service.config import settings
import uvicorn

from api.v1 import recommendations_api

app = FastAPI(
    title=settings.project_name,
    docs_url='/api_recommendations/openapi',
    openapi_url='/api_recommendations/openapi.json',
    # Changing default JSON serializer to optimized version.
    default_response_class=ORJSONResponse,
)


app.include_router(recommendations_api.router, prefix='/api/v1/recommendations', tags=['recommendations'])

if __name__ == '__main__':
    # The app can also be run by `uvicorn main:app --host 0.0.0.0 --port 8003` cmd.
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8003,
    )
