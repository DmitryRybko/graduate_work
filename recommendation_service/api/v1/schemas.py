from pydantic import BaseModel


class RecommendationsRequest(BaseModel):
    """Запрос на сохранение данных."""
    key: str
    value: str


class RecommendationsResponse(BaseModel):
    """Запрос на сохранение данных."""
    key: str
    value: str
