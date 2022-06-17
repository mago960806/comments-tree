from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .vo import Email


@dataclass
class User:
    """
    User Entity
    """

    username: str
    password: str
    email: Email
    id: Optional[int] = None
    is_active: bool = True
    is_superuser: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
