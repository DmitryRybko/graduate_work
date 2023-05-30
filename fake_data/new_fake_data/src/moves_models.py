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
