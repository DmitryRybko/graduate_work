"""Movies DB utils module."""

import random
from datetime import date
from uuid import uuid4

from faker import Faker

from sqlalchemy import func
from sqlalchemy.orm import load_only

from werkzeug.security import generate_password_hash

from data.genres import genre_list
from movies_models import (
    Genre, GenreFilmWork, FilmWork, Person, PersonFilmWork
)
from settings import settings


director_role_name = 'director'
actor_role_name = 'actor'
writer_role_name = 'writer'

fake: Faker = Faker(['it_IT', 'en_US', 'de_DE', 'fr_FR'])


def generate_genres(session) -> None:
    """Generate test data in genre table of movies_db."""
    if len(genre_list) <= settings.genre_size:
        end_item: int = len(genre_list)
    else:
        end_item = int(settings.genres_size)
    for genre_name in genre_list[:end_item]:
        session.add(
            Genre(name=genre_name, description=fake.text())
        )
    session.commit()
    session.flush()


def generate_persons(session) -> None:
    """Generate fake persons."""
    i: int = 0
    person_in_session: int = 0
    while i < settings.person_size:
        session.add(Person(full_name=fake.name()))
        person_in_session

        if person_in_session >= settings.batch_size:
            session.commit()
            session.flush()
            person_in_session = 0
        i += 1
    session.commit()
    session.flush()


def generate_new_person(session) -> None:
    """Create a new person."""
    session.add(Person(full_name=fake.name()))
    session.commit()
    session.flush()


def get_persons_for_a_film_work(session) -> list[dict]:
    """Return list of persons to add in film_work."""
    director_size = random.randint(1, 3)
    actor_size = random.randint(3, 10)
    writer_size = random.randint(1, 3)
    person_size = sum((director_size, actor_size, writer_size))

    person_from_db = session.query(Person).options(load_only('id')).offset(
        func.floor(
            func.random() *
            session.query(func.count(Person.id))
        )
    ).limit(person_size).all()

    persons: list[dict] = [
        {
            'id': p.id, 'type': director_role_name
        } for p in person_from_db[:director_size]
    ]
    persons += [
        {
            'id': p.id, 'type': director_role_name
        } for p in person_from_db[director_size:actor_size+director_size]
    ]
    persons += [
        {
            'id': p.id, 'type': director_role_name
        } for p in person_from_db[actor_size+director_size:]
    ]
    return persons


def generate_film_works(session) -> None:
    """Generate film_works in movies db."""
    session_size: int = 0
    for i in range(settings.film_work_size):
        persons = get_persons_for_a_film_work(session)

        genres_from_db = session.query(Genre).options(load_only('id')).offset(
            func.floor(
                func.random() *
                session.query(func.count(Genre.id))
            )
        ).limit(random.randint(1, 5)).all()

        session.add(
            film_work := FilmWork(
                id=uuid4(),
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
        session_size += 1

        for person in persons:
            session.add(
                PersonFilmWork(
                    person_id=person['id'],
                    film_work_id=film_work.id,
                    role=person['type']
                )
            )
            session_size += 1

        for genre in genres_from_db:
            session.add(
                GenreFilmWork(
                    genre_id=genre.id,
                    film_work_id=film_work.id
                )
            )
            session_size += 1

        if session_size >= settings.batch_size:
            session.commit()
            session.flush()
            session_size = 0

    session.commit()
    session.flush()


def generate_a_new_film_work(session) -> None:
    persons = get_persons_for_a_film_work(session)

    genres_from_db = session.query(Genre).options(load_only('id')).offset(
        func.floor(
            func.random() *
            session.query(func.count(Genre.id))
        )
    ).limit(random.randint(1, 5)).all()

    session.add(
        film_work := FilmWork(
            id=uuid4(),
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

    for person in persons:
        session.add(
            PersonFilmWork(
                person_id=person['id'],
                film_work_id=film_work.id,
                role=person['type']
            )
        )

    for genre in genres_from_db:
        session.add(
            GenreFilmWork(
                genre_id=genre.id,
                film_work_id=film_work.id
            )
        )

    session.commit()
    session.flush()


def get_random_film_works(session, limit: int = 10) -> list[FilmWork]:
    """Return list of film_work items."""
    film_work_from_db = session.query(
        FilmWork
    ).offset(
        func.floor(
            func.random() *
            session.query(func.count(FilmWork.id))
        )
    ).limit(limit).all()
    return film_work_from_db
