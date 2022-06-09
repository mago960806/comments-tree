from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Comment:
    """
    Comment Entity
    """

    id: int
    content: str
    parent_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
