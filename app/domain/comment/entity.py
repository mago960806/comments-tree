from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class Comment:
    """
    Comment Entity
    """

    content: str
    id: Optional[int] = None
    children: List["Comment"] = field(default_factory=lambda: [])
    parent_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
