"""
Import all SQLAlchemy models here.
Alembic uses this file to discover tables.
"""

from maku_todo.app.components.auth.models import User
from maku_todo.app.components.todo.models import Todo