"""Test config module."""

import os

import pytest

from ...config import Config


def test_config():
    project_name = 'test project name'
    os.environ['project_name'] = project_name
    redis_host = 'redis-hostname'
    os.environ['redis_host'] = redis_host
    redis_port = '6379'
    os.environ['redis_port'] = redis_port
    redis_db = '5'
    os.environ['redis_db'] = redis_db

    settings: Config = Config()

    assert settings.project_name == project_name
    assert settings.redis_host == redis_host
    assert settings.redis_port == redis_port
    assert settings.redis_db == redis_db
