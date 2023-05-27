"""Test models module."""

from pytest.mark import parametrize

from ...api.v1.recommendations_api import RecommendationsResponse


@parametrize(
    'test_data',
    (
        [],
        [f'film_id_{i}' for i in range(10)],
        [f'{i}' for i in range(100)]
    )
)
def test_recomandation_response(test_data: list):
    rr: RecommendationsResponse = RecommendationsResponse(movies_id=test_data)
    assert rr.movies_id == test_data
