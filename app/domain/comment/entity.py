from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Comment:
    """
    Comment Entity
    """

    content: str
    id: Optional[int] = None
    parent_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
