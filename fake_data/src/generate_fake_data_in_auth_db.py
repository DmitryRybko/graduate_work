#!/usr/bin/env python3
"""Main script to generate fake data in movies DB."""

# default libs
import random
from datetime import datetime, timedelta
from time import sleep
from typing import Generator
from uuid import uuid4

# third party libs
import psycopg2
from faker import Faker
from werkzeug.security import generate_password_hash

# project imports
import models
from settings import settings
from utils import wait_db


fake: Faker = Faker(['it_IT', 'en_US', 'ja_JP', 'de_DE', 'fr_FR'])


def wait_when_all_tables_available(timeout_min: int = 2):
    """Wait when all tables is available."""
    print(settings.auth_db_connect_data)
    with psycopg2.connect(
        **settings.auth_db_connect_data
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
                        f'SELECT count(*) FROM "{table}"'
                    )
            except Exception as e:
                print(e)
                sleep(1)
                timeout -= 1
            else:
                return
        raise Exception('Exception. Timeout. Waiting of tables.')


def write_to_db(table_name: str, values: list, conflict_by_id: bool = True):
    """Write data to the DB."""
    with psycopg2.connect(
        **settings.auth_db_connect_data
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
        sql: str = f'INSERT INTO "{table_name}" ({fields_str}) VALUES {args}'
        if conflict_by_id:
            sql += ' ON CONFLICT (id) DO NOTHING;'
        try:
            pg_cur.execute(sql)
        except psycopg2.errors.UniqueViolation as e:
            print(e)


def data_getter(sql: str) -> Generator:
    """Return data by sql request."""
    with psycopg2.connect(
        **settings.auth_db_connect_data
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
    """Generate test roles."""
    roles: list[models.Role] = [
        models.Role(
            id=str(uuid4()), name=f'Test role #{i}'
        ) for i in range(settings.role_size)
    ]
    write_to_db(settings.auth_role_table_name, roles)


def generate_users() -> None:
    """Generate test users."""
    users: list[models.User] = []
    for i in range(settings.user_size):
        first_name: str = fake.first_name()
        last_name: str = fake.last_name()
        email: str = f'{first_name}.{last_name}@{fake.domain_name()}'
        user_id = str(uuid4())
        users.append(
            models.User(
                id=user_id,
                email=email,
                name=f'{first_name} {last_name}',
                password=generate_password_hash(first_name+last_name),
                is_admin=False
            )
        )
        generate_user_role(user_id)
        generate_log_history(user_id)
        if len(users) >= settings.batch_size:
            write_to_db(settings.auth_user_table_name, users)
            users = []
    if users:
        write_to_db(settings.user_table_name, users)


def generate_user_role(user_id: str) -> None:
    """Generate user-role connections."""
    user_role: list[models.UserRole] = []
    for data in data_getter(
        f'SELECT id FROM "{settings.auth_role_table_name}"'
    ):
        for role in data:
            user_role.append(
                models.UserRole(
                    user_id=user_id, role_id=role[0]
                )
            )
            if len(user_role) >= settings.batch_size:
                write_to_db(
                    settings.auth_user_role_table_name, user_role, False
                )
    if user_role:
        write_to_db(settings.auth_user_role_table_name, user_role, False)


def generate_log_history(user_id: str) -> None:
    """Generate test login history data."""
    log_history: list[models.LogHistory] = []
    cur = datetime.now()
    for i in range(random.randint(1, settings.log_history)):
        delta = timedelta(hours=random.randint(1, 100000))
        timestamp = cur - delta
        log_history.append(
            models.LogHistory(
                id=str(uuid4()),
                user_id=user_id,
                log_time=timestamp.strftime('%Y-%m-%d %H:%M:%S')
            )
        )
        if len(log_history) >= settings.batch_size:
            write_to_db(settings.auth_log_history_table_name, log_history)
    if log_history:
        write_to_db(settings.auth_log_history, log_history)


def main():
    """Generate fake data."""
    if settings.debug:
        wait_db.main()
        wait_when_all_tables_available()

        generate_roles()
        generate_users()


if __name__ == '__main__':
    main()
