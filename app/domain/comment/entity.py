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
    parent_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class CommentTreeNode:
    """
    Comment Tree Node Entity
    """

    content: str
    id: Optional[int] = None
    children: List["CommentTreeNode"] = field(default_factory=lambda: [])
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
