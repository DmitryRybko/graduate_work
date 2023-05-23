#!/usr/bin/env python3
"""Main script to generate fake data in movies DB."""

# default libs
import random
from datetime import date
from time import sleep
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


def wait_when_all_tables_available(timeout_min: int = 2):
    """Wait when all tables is available."""
    with psycopg2.connect(
        **settings.auth_db_connect_data()
    ) as pg_conn, pg_conn.cursor() as pg_cur:
        timeout = timeout_min * 60
        tables = (
            settings.auth_user_table_name,
            settings.auth_role_table_name,
            settings.auth_log_history_table_name
        )
        while timeout > 0:
            try:
                for table in tables:
                    pg_cur.execute(
                        f'SELECT count(*) FROM {table}'
                    )
            except Exception as e:
                print(e)
                sleep(1)
                timeout -= 1
            else:
                return
        raise Exception('Exception. Timeout. Waiting of tables.')


def write_to_db(table_name: str, values: list):
    """Write data to the DB."""
    with psycopg2.connect(
        **settings.auth_db_connect_data()
    ) as pg_conn, pg_conn.cursor() as pg_cur:
        fields: list = [k for k, v in values[0].dict().items()]
        items_in_request: str = ', '.join(
            ['%s' for _ in range(len(fields))]
        )
        args_list: list = [
            tuple(
                [i.dict()[f] for f in fields]
            ) for i in values
        ]
        args: str = ','.join(
            pg_cur.mogrify(
                f'({items_in_request})', item
            ).decode() for item in args_list
        )
        fields_str: str = ', '.join(fields)
        sql: str = f'INSERT INTO {table_name} ({fields_str}) VALUES {args}'
        pg_cur.execute(sql)


def data_getter(sql: str) -> Generator:
    with psycopg2.connect(
        **settings.auth_db_connect_data()
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


def generate_roles() -> None:
    pass


def generate_users() -> None:
    pass


def generate_log_history():
    pass


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
    if genres:
        write_to_db(settings.genre_table_name, genres)


def generate_filmworks() -> None:
    """Generate fake filmworks."""
    i: int = 0
    filmworks: list[models.Filmwork] = []
    while i < settings.filmwork_size:
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
        i += 1
    if filmworks:
        write_to_db(settings.filmwork_table_name, filmworks)


def generate_persons() -> None:
    """Generate fake persons."""
    i: int = 0
    persons: list[models.Person] = []
    while i < settings.person_size:
        persons.append(
            models.Person(
                id=str(uuid4()),
                full_name=fake.name()
            )
        )
        if len(persons) >= settings.batch_size:
            write_to_db(settings.person_table_name, persons)
            persons = []
        i += 1
    if persons:
        write_to_db(settings.person_table_name, persons)


def generate_genre_filmwork() -> None:
    """Generate relations between genre and filmwork."""
    genre_filmworks: list[models.GenreFilmwork] = []
    for data in data_getter(f'SELECT id FROM {settings.filmwork_table_name}'):
        for film in data:
            genres = [
                i for i in data_getter(
                    (
                        f'SELECT id from {settings.genre_table_name} '
                        f'ORDER BY RANDOM() LIMIT {random.randint(1, 5)}'
                    )
                )
            ][0]
            for genre in genres:
                genre_filmworks.append(
                    models.GenreFilmwork(
                        id=str(uuid4()),
                        film_work_id=film[0],
                        genre_id=genre[0]
                    )
                )
        write_to_db(settings.genre_filmwork_table_name, genre_filmworks)
        genre_filmworks = []


def generate_person_filmwork() -> None:
    """Generate relations between person and filmwork."""
    person_filmworks: list[models.PersonFilmwork] = []
    for data in data_getter(f'SELECT id FROM {settings.filmwork_table_name}'):
        for film in data:
            director_size = random.randint(1, 3)
            actor_size = random.randint(3, 10)
            writer_size = random.randint(1, 3)
            person_size = sum((director_size, actor_size, writer_size))

            person_from_db = [
                i for i in data_getter(
                    (
                        f'SELECT id FROM {settings.person_table_name} '
                        f'ORDER BY RANDOM() LIMIT {person_size}'
                    )
                )
            ][0]

            director_ids = person_from_db[:director_size]
            actor_ids = person_from_db[director_size:actor_size+director_size]
            writer_ids = person_from_db[actor_size+director_size:]

            # print(writer_ids)
            person_sets: tuple = (
                {'items': director_ids, 'type': 'director'},
                {'items': actor_ids, 'type': 'actor'},
                {'items': writer_ids, 'type': 'writer'}
            )
            for person_set in person_sets:
                for person in person_set['items']:
                    person_filmworks.append(
                        models.PersonFilmwork(
                            id=str(uuid4()),
                            film_work_id=film[0],
                            person_id=person[0],
                            role=person_set['type']
                        )
                    )
            if len(person_filmworks) >= settings.batch_size:
                write_to_db(
                    settings.person_filmwork_table_name, person_filmworks
                )
                person_filmworks = []
    if person_filmworks:
        write_to_db(settings.person_filmwork_table_name, person_filmworks)


def main():
    """Generate fake data."""
    if settings.debug:
        wait_db.main()
        wait_when_all_tables_available()

        generate_genres()
        generate_persons()
        generate_filmworks()

        generate_genre_filmwork()
        generate_person_filmwork()


if __name__ == '__main__':
    main()
