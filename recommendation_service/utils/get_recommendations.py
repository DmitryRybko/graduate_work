import requests
from http import HTTPStatus
from loguru import logger

from recommendation_service.config import settings


def get_viewed_movies(user_id: str) -> list | None:
    """Return list of user's viewed films."""

    logger.debug(f"getting views data for user {user_id}")

    url: str = f"{settings.get_watching_history_url}/{user_id}"

    response = requests.get(url)

    if response.status_code == HTTPStatus.OK:
        data = response.json()
        movies_list: list | None = data[user_id]
        logger.debug(f"data received: {data}")
    else:
        logger.error("Error: Failed to retrieve data from API")
        movies_list = None
    return movies_list


def get_genres_for_movies(movies: list) -> list | None:
    """Return list of genres for movies list."""
    logger.debug(f"getting genre data for movies")

    url: str = settings.get_genres_url
    data: dict = {"movies": movies}

    response = requests.post(url, json=data)

    if response.status_code == HTTPStatus.OK:
        response_data = response.json()
        logger.debug(f"{response_data}")
        genres_list = response_data["genre_ids"]
        return genres_list
    else:
        logger.debug("Error: ", response.status_code)


def most_frequent_genre(genres: list) -> str | None:
    """Return the most frequent genre."""
    # Create a dictionary to store the frequency of each genre
    genre_freq = {}
    for genre in genres:
        if genre in genre_freq:
            genre_freq[genre] += 1
        else:
            genre_freq[genre] = 1

    # Find the genre with the highest frequency
    max_freq = 0
    most_frequent = None
    for genre, freq in genre_freq.items():
        if freq > max_freq:
            max_freq = freq
            most_frequent = genre
    logger.debug(f"favourite genre: {most_frequent}")
    return most_frequent


def get_recommended_movies(genre: str) -> dict | str:
    """Return recommended movies by genre name."""
    url: str = settings.get_recommendations_url
    data: dict = {"genre": genre}

    response = requests.post(url, json=data)

    if response.status_code == HTTPStatus.OK:
        logger.debug(f"{response}")
        logger.debug(f"{response.json()}")
        return response.json()
    else:
        return "Error: " + str(response.status_code)


def get_default_movies() -> dict | str:
    """Return recommended movies to a default user."""

    url: str = settings.default_recommendations_url
    logger.info(f"getting default movies at {url}")
    response = requests.get(url)
    logger.info(f"response {response}")
    if response.status_code == HTTPStatus.OK:
        logger.debug(f"{response}")
        logger.debug(f"{response.json()}")
        return response.json()
    else:
        return "Error: " + str(response.status_code)


def get_recommendations(user_id: str) -> dict | None:
    """Return recommended films for a user."""

    if user_id == "default_user":
        recommended_movies: dict | None = get_default_movies()
    else:
        viewed_movies: list | None = get_viewed_movies(user_id)
        if viewed_movies is None:
            return None
        user_genres = get_genres_for_movies(viewed_movies)
        if user_genres is None:
            return None
        user_top_genre = most_frequent_genre(user_genres)
        if user_top_genre is None:
            return None
        recommended_movies: dict | None = get_recommended_movies(user_top_genre)
    return recommended_movies


if __name__ == '__main__':
    # example usage
    viewed_movies = get_viewed_movies("email2@emails.ru")
    user_genres = get_genres_for_movies(viewed_movies)
    user_top_genre = most_frequent_genre(user_genres)
    recommended_movies = get_recommended_movies(user_top_genre)

    # get_default_movies()
