from pydantic import BaseModel


class RecommendationsResponse(BaseModel):
    movies_id: list

