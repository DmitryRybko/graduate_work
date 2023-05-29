from pydantic import BaseModel


class RecommendationsResponse(BaseModel):
    movies_data: dict[str, dict]

