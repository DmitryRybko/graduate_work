"""Auth models module."""

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

user_role = Table(
    settings.user_role_table_name,
    Base.metadata,
    Column(
        'user_id', UUID(as_uuid=True), ForeignKey('user.id', ondelete='CASCADE')
    ),
    Column(
        'role_id', UUID(as_uuid=True), ForeignKey('role.id', ondelete='CASCADE')
    )
)


class LogHistory(Base):
    __tablename__ = settings.log_history_table_name

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    log_time = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'))


class Role(Base):
    __tablename__ = settings.role_table_name
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    name = Column(String(100), unique=True)

    def __repr__(self):
        return f"<Role {self.name}>"


class User(Base):
    __tablename__ = settings.user_table_name
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )

    email = Column(String(100), unique=True)
    password = Column(String(100))
    name = Column(String(1000))
    is_admin = Column(Boolean)
    log_history = relationship('LogHistory')

    roles = relationship(
        'Role',
        secondary=user_role,
        backref='users',
        cascade='delete'
    )

    def __repr__(self):
        return f'<User {self.name}>'
