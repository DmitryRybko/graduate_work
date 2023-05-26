#!/usr/bin/env python3
"""Models module."""

from datetime import date, datetime
# from uuid import UUID

from pydantic import BaseModel


class Person(BaseModel):
    """Person model."""

    id: str
    full_name: str
    created: datetime = datetime.now()
    modified: datetime = datetime.now()


class Genre(BaseModel):
    """Genre model."""

    id: str
    name: str
    description: str
    created: datetime = datetime.now()
    modified: datetime = datetime.now()


class Filmwork(BaseModel):
    """Filmwork model."""

    id: str
    title: str
    description: str
    creation_date: date
    rating: float
    type: str
    created: datetime = datetime.now()
    modified: datetime = datetime.now()


class GenreFilmwork(BaseModel):
    """Many_to_many relationship between Genre and Filmwork."""

    id: str
    created: datetime = datetime.now()
    film_work_id: str
    genre_id: str


class PersonFilmwork(BaseModel):
    """Many_to_many relationship between Person and Filmwork."""

    id: str
    created: datetime = datetime.now()
    role: str
    film_work_id: str
    person_id: str


class Role(BaseModel):
    id: str
    name: str


class User(BaseModel):
    id: str
    email: str
    password: str
    name: str
    is_admin: bool


class UserRole(BaseModel):
    user_id: str
    role_id: str


class LogHistory(BaseModel):
    id: str
    log_time: datetime
    user_id: str


class WatchingHistory(BaseModel):
    film_id: str
