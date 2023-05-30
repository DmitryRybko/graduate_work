"""Movies models module."""

import uuid

# import sqlalchemy as db
from sqlalchemy import func
from sqlalchemy import (
    Table, Column, ForeignKey, DateTime, String, Boolean
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from settings import settings


Base = declarative_base()

class PersonFilmWork(Base):
    __tablename__ = settings.person_film_work_table_name
    schema = settings.movies_schema_name
    person_id = Column(
        UUID(as_uuid=True), ForeignKey(f'user.id', ondelete='CASCADE')
    ),
    film_work_id = Column(
        UUID(as_uuid=True), ForeignKey('role.id', ondelete='CASCADE')
    ),
    role = Column(String),
    created = (DateTime(timezone=True), server_default=func.now())


class FilmWork(Base):
    __tablename__ = settings.filmwork_table_name
    schema = settings.movies_schema_name

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    
    def __repr__(self):
        return f"<FilmWork: {self.title}>"


class Genre(Base):
    __tablename__ = settings.genre_table_name
    schema = settings.movies_schema_name

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
        String,
        nullable=True
    )
    
    def __repr__(self):
        return f"<Genre: {self.title}>"

class Person(Base):
    __tablename__ = settings.person_table_name
    schema = settings.movies_schema_name

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
    
    def __repr__(self):
        return f"<Person: {self.title}>"