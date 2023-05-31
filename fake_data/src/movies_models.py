"""Movies models module."""

import uuid
from datetime import datetime

# import sqlalchemy as db
from sqlalchemy import func
from sqlalchemy import (
    Column, Date, DateTime, Float, ForeignKey, String
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from settings import settings


Base = declarative_base()


class GenreFilmWork(Base):
    __tablename__ = settings.genre_film_work_table_name
    __table_args__ = {'schema': settings.movies_schema_name}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    genre_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            f'{settings.movies_schema_name}.{settings.genre_table_name}.id',
            ondelete='CASCADE'
        )
    )
    film_work_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            f'{settings.movies_schema_name}.{settings.film_work_table_name}.id',
            ondelete='CASCADE'
        )
    )
    created = Column(DateTime(timezone=True), default=datetime.now())


class PersonFilmWork(Base):
    __tablename__ = settings.person_film_work_table_name
    __table_args__ = {'schema': settings.movies_schema_name}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    person_id = Column(
        UUID(as_uuid=True),
        ForeignKey(f'{settings.movies_schema_name}.{settings.film_work_table_name}.id', ondelete='CASCADE')
    )
    film_work_id = Column(
        UUID(as_uuid=True),
        ForeignKey(f'{settings.movies_schema_name}.{settings.genre_table_name}.id', ondelete='CASCADE')
    )
    role = Column(String),
    created = Column(DateTime(timezone=True), default=datetime.now())


class Genre(Base):
    __tablename__ = settings.genre_table_name
    __table_args__ = {'schema': settings.movies_schema_name}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    name = Column(
        String(255),
        nullable=False
    )
    description = Column(
        String(),
        nullable=True
    )
    created = Column(DateTime(timezone=True), default=datetime.now())
    modified = Column(DateTime(timezone=True), default=datetime.now())

    def __repr__(self):
        return f'<Genre: {self.title}>'


class Person(Base):
    __tablename__ = settings.person_table_name
    __table_args__ = {'schema': settings.movies_schema_name}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    full_name = Column(
        String(255),
        nullable=False
    )
    created = Column(DateTime(timezone=True), default=datetime.now())
    modified = Column(DateTime(timezone=True), default=datetime.now())

    def __repr__(self):
        return f'<Person: {self.title}>'


class FilmWork(Base):
    __tablename__ = settings.film_work_table_name
    __table_args__ = {'schema': settings.movies_schema_name}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    created = Column(DateTime(timezone=True), default=datetime.now())
    modified = Column(DateTime(timezone=True), default=datetime.now())
    title = Column(String(255), nullable=False)
    description = Column(String(), nullable=True)
    creation_date = Column(Date(), nullable=True)
    rating = Column(Float(), nullable=True)
    type = Column(String(100))
    genres = relationship('GenreFilmWork')
    persons = relationship('PersonFilmWork')

    def __repr__(self):
        return f'<FilmWork: {self.title}>'
