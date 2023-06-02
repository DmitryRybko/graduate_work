"""Auth utils module."""

import random
from typing import Generator

from faker import Faker

from sqlalchemy import func
from sqlalchemy.orm import load_only

from werkzeug.security import generate_password_hash

from auth_models import Role, User
from logger import get_logger
from settings import settings

logger = get_logger()


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
    """Generate only one user."""
    logger.debug('Generating new user')
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
        user := User(
            email=email,
            password=generate_password_hash(
                first_name+last_name, method='sha256'
            ),
            name=f'{first_name} {last_name}',
            is_admin=False,
            roles=roles
        )
    )
    logger.debug(user)
    session.commit()


def get_all_users(session) -> Generator:
    """Return all users one by one."""
    logger.debug('Get all users')
    users = session.query(User).all()
    for user in users:
        yield user


def get_random_user(session) -> str:
    """Return one random user."""
    logger.debug('Get random user')
    users = session.query(User).options(load_only('id')).offset(
        func.floor(
            func.random() *
            session.query(func.count(User.id))
        )
    ).limit(1).all()
    logger.debug('Random user: ' + str(users[0]))
    return users[0]
