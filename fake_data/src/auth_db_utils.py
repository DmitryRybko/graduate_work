"""Auth utils module."""

import random
from typing import Generator

from faker import Faker

from sqlalchemy import func
from sqlalchemy.orm import load_only

from werkzeug.security import generate_password_hash

from auth_models import Role, User
from settings import settings


fake: Faker = Faker(['it_IT', 'en_US', 'de_DE', 'fr_FR'])


def generate_roles(session) -> None:
    """Generate roles in Auth db."""
    roles: int = 0
    for i in range(settings.role_size):
        session.add(Role(name=f'Role #{i}'))
        if roles >= settings.batch_size:
            session.commit()
            session.flush()
            roles = 0
    session.commit()
    session.flush()


def generate_users(session) -> None:
    """Generate users in Auth DB."""
    users: int = 0
    for i in range(settings.user_size):
        first_name: str = fake.first_name()
        last_name: str = fake.last_name()
        email: str = f'{first_name}.{last_name}@{fake.domain_name()}'

        roles = session.query(Role).options(load_only('id')).offset(
            func.floor(
                func.random() *
                session.query(func.count(Role.id))
            )
        ).limit(random.randint(1, settings.user_role_size)).all()

        session.add(
            User(
                email=email,
                password=generate_password_hash(
                    first_name+last_name, method='sha256'
                ),
                name=f'{first_name} {last_name}',
                is_admin=False,
                roles=roles
            )
        )
        if users >= settings.batch_size:
            session.commit()
            session.flush()
            users = 0
    session.commit()
    session.flush()


def generate_a_new_user(session) -> None:
    first_name: str = fake.first_name()
    last_name: str = fake.last_name()
    email: str = f'{first_name}.{last_name}@{fake.domain_name()}'

    roles = session.query(Role).options(load_only('id')).offset(
        func.floor(
            func.random() *
            session.query(func.count(Role.id))
        )
    ).limit(random.randint(1, settings.user_role_size)).all()

    session.add(
        User(
            email=email,
            password=generate_password_hash(
                first_name+last_name, method='sha256'
            ),
            name=f'{first_name} {last_name}',
            is_admin=False,
            roles=roles
        )
    )
    session.commit()


def get_all_users(session) -> Generator:
    """Return all users one by one."""
    users = session.query(User).all()
    for user in users:
        yield user
