import requests
from loguru import logger

from config import settings


def get_viewed_movies(user_id):
    logger.debug(f"getting views data for user {user_id}")
    url = f"{settings.get_warching_history_url}/{user_id}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        movies_list = data[user_id]
        logger.debug(f"data received: {data}")
    else:
        logger.error("Error: Failed to retrieve data from API")
        movies_list = None
    return movies_list


def get_genres_for_movies(movies: list):
    logger.debug("getting genre data for movies")

    url = settings.get_genres_url
    data = {"movies": movies}

    response = requests.post(url, json=data)

    if response.status_code == 200:
        response_data = response.json()
        logger.debug(f"{response_data}")
        genres_list = response_data["genre_ids"]
        return genres_list
    else:
        logger.debug("Error: ", response.status_code)


def most_frequent_genre(genres):
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


def get_recommended_movies(genre):
    url = settings.get_recommendations_url
    data = {"genre": genre}

    response = requests.post(url, json=data)

    if response.status_code == 200:
        logger.debug(f"{response}")
        logger.debug(f"{response.json()}")
        return response.json()
    else:
        return "Error: " + str(response.status_code)


def get_recommendations(user_id):
    viewed_movies = get_viewed_movies(user_id)
    user_genres = get_genres_for_movies(viewed_movies)
    user_top_genre = most_frequent_genre(user_genres)
    recommended_movies = get_recommended_movies(user_top_genre)
    return recommended_movies


if __name__ == '__main__':
    viewed_movies = get_viewed_movies("email2@emails.ru")
    user_genres = get_genres_for_movies(viewed_movies)
    user_top_genre = most_frequent_genre(user_genres)
    recommended_movies = get_recommended_movies(user_top_genre)
