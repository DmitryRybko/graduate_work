#!/usr/bin/env python3

import random
from typing import Generator

import psycopg2
from motor.motor_asyncio import AsyncIOMotorClient

from settings import settings


def data_getter(ps_connect_data: dict, sql: str) -> Generator:
    """Return data by sql request."""
    with psycopg2.connect(
        **ps_connect_data
    ) as pg_conn, pg_conn.cursor() as pg_cur:
        # print(sql)
        pg_cur.execute(sql)
        while True:
            data_part = pg_cur.fetchmany(1000)
            if data_part:
                # print(data_part)
                yield data_part
            else:
                return


def user_getter() -> Generator:
    """Return generator to get all user_id from users db."""
    for part_users in data_getter(
        settings.auth_db_connect_data,
        f'SELECT id from "{settings.auth_user_table_name}"'
    ):
        for user in part_users:
            yield user[0]


def film_list_getter(limit: int) -> Generator:
    """Return list of random films."""
    for part_of_films in data_getter(
        settings.movie_db_connect_data,
        (
            f'SELECT id from {settings.filmwork_table_name} '
            f'ORDER BY RANDOM() LIMIT {limit}'
        )
    ):
        for film in part_of_films:
            yield film[0]


def main() -> None:
    client: AsyncIOMotorClient = AsyncIOMotorClient(settings.mongo_db_url)
    db = client[settings.mongo_db_db_name]
    film_list: list[dict] = []
    for user_id in user_getter():
        for film_id in film_list_getter(
            random.randint(0, settings.watching_history_size)
        ):
            film_list.append({'film_id': film_id})
            if len(film_list) >= settings.batch_size:
                db[user_id].insert_many(film_list)
        if film_list:
            db[user_id].insert_many(film_list)


if __name__ == '__main__':
    main()
