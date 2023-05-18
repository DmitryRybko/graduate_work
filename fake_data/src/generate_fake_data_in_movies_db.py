#!/usr/bin/env python3
"""Main script to generate fake data in movies DB."""

# default libs
import random
from datetime import date
from typing import Generator
from uuid import uuid4

# third party libs
import psycopg2
from faker import Faker

# project imports
import models
from genres import genre_list
from settings import settings
from utils import wait_db


fake: Faker = Faker(['it_IT', 'en_US', 'ja_JP', 'de_DE', 'fr_FR'])


def write_to_db(table_name: str, values: list):
    """Write data to the DB."""
    print(table_name)
    print(values)
    with psycopg2.connect(
        dbname=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT
    ) as pg_conn, pg_conn.cursor() as pg_cur:
        fields: list = [k for k, v in values[0].dict().items()]
        print(fields)
        items_in_request: str = ', '.join(
            ['%s' for _ in range(len(fields))]
        )
        print(items_in_request)
        args_list: list = [
            tuple(
                [i.dict()[f] for f in fields]
            ) for i in values
        ]
        print(args_list)
        args: str = ','.join(
            pg_cur.mogrify(
                f'({items_in_request})', item
            ).decode() for item in args_list
        )
        sql: str = f'INSERT INTO {table_name} ({fields}) VALUES {args}'
        pg_cur.execute(sql)


def data_getter(sql: str) -> Generator:
    with psycopg2.connect(
        dbname=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT
    ) as pg_conn, pg_conn.cursor() as pg_cur:
        pg_cur.execute(sql)
        while True:
            data_part = pg_cur.fetchmany(1000)
            if data_part:
                yield data_part
            else:
                return


def generate_genres() -> None:
    """Generate fake genres."""
    genres: list[models.Genre] = []
    if len(genre_list) <= settings.genres_size:
        end_item: int = len(genre_list)
    else:
        end_item = int(settings.genres_size)
    for i in genre_list[:end_item]:
        genres.append(
            models.Genre(id=str(uuid4()), name=i, description=fake.text())
        )
    write_to_db(settings.genre_table_name, genres)


def generate_filmworks() -> None:
    """Generate fake filmworks."""
    i: int = 0
    while i < settings.filmwork_size:
        filmworks: list[models.Filmwork] = []
        filmworks.append(
            models.Filmwork(
                id=str(uuid4()),
                title=fake.sentence(nb_words=random.randint(2, 10)),
                description=fake.text(),
                creation_date=date(
                    random.randint(1922, 2022),
                    random.randint(1, 12),
                    random.randint(1, 28)
                ),
                rating=random.uniform(1.1, 9.9),
                type=random.choice(('film', 'tv show', 'serial'))
            )
        )
        if len(filmworks) >= settings.batch_size:
            write_to_db(settings.filmwork_table_name, filmworks)
            filmworks = []
    write_to_db(settings.filmwork_table_name, filmworks)


def generate_persons() -> None:
    """Generate fake persons."""
    i: int = 0
    while i < settings.person_size:
        persons: list[models.Person] = []
        persons.append(
            models.Person(
                id=str(uuid4()),
                full_name=fake.name()
            )
        )
        if len(persons) >= settings.batch_size:
            write_to_db(settings.person_table_name, persons)
            persons = []
    write_to_db(settings.person_table_name, persons)


def generate_genre_filmwork() -> None:
    """Generate relations between genre and filmwork."""
    for data in data_getter(f'SELECT id FROM {settings.filmwork_table_name}'):
        for i in data:
            genre_ids = [
                i[0] for i in data_getter(
                    (
                        f'SELECT id from {settings.genre_table_name} '
                        f'ORDER BY RAND() LIMIT {random.randint(1, 5)}'
                    )
                )
            ]
            for genre_id in genre_ids:
                genre_filmworks: list[models.GenreFilmwork] = []
                genre_filmworks.append(
                    models.GenreFilmwork(
                        id=str(uuid4()),
                        film_work_id=i[0],
                        genre_id=genre_id
                    )
                )
            write_to_db(settings.genre_filmwork_table_name, genre_filmworks)
            genre_filmworks = []


def generate_person_filmwork() -> None:
    """Generate relations between person and filmwork."""
    for data in data_getter(f'SELECT id FROM {settings.filmwork_table_name}'):
        for i in data:
            director_ids = [
                i[0] for i in data_getter(
                    (
                        f'SELECT id from {settings.person_table_name} '
                        f'ORDER BY RAND() LIMIT {random.randint(1, 3)}'
                    )
                )
            ]
            actor_ids = [
                i[0] for i in data_getter(
                    (
                        f'SELECT id from {settings.person_table_name} '
                        f'ORDER BY RAND() LIMIT {random.randint(3, 10)}'
                    )
                )
            ]
            writer_ids = [
                i[0] for i in data_getter(
                    (
                        f'SELECT id from {settings.person_table_name} '
                        f'ORDER BY RAND() LIMIT {random.randint(1, 3)}'
                    )
                )
            ]
            person_sets: tuple = (
                {'items': director_ids, 'type': 'director'},
                {'items': actor_ids, 'type': 'actor'},
                {'items': writer_ids, 'type': 'writer'}
            )
            for person_set in person_sets:
                for i in person_set['items']:
                    person_filmworks: list[models.PersonFilmwork] = []
                    person_filmworks.append(
                        models.PersonFilmwork(
                            id=str(uuid4()),
                            film_work_id=i[0],
                            person_id=i,
                            role=person_set['type']
                        )
                    )
                write_to_db(
                    settings.genre_filmwork_table_name, person_filmworks
                )
                person_filmworks = []


def main():
    """Generate fake data."""
    if settings.debug:
        wait_db.main()
        print(settings)
        generate_genres()
        generate_persons()
        generate_filmworks()

        generate_genre_filmwork()
        generate_person_filmwork()


if __name__ == '__main__':
    main()
