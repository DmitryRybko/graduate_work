from pydantic import BaseModel


class RecommendationsResponse(BaseModel):
    """Запрос на сохранение данных."""
    key: str
    value: str
