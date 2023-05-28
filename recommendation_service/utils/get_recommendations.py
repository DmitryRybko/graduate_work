import requests
from loguru import logger


def get_viewed_movies(user_id):
    logger.debug(f"getting views data for user {user_id}")
    url = f"http://localhost:8014/api/v1/history/get/{user_id}"
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
    logger.debug(f"getting genre data for movies")

    url = "http://localhost:8001/api/v1/films/get_genres"
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


if __name__ == '__main__':
    viewed_movies = get_viewed_movies("email2@emails.ru")
    user_genres = get_genres_for_movies(viewed_movies)
    user_top_genre = most_frequent_genre(user_genres)
