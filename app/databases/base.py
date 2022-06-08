from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import declarative_base, declared_attr


class TimestampMixin(object):
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=True)


class Base:
    """
    扩展模型基类, 根据类名称自动生成表名
    """

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


class TimestampBase(Base, TimestampMixin):
    """
    提供创建时间与更新时间字段的基类
    """

    pass


BaseModel = declarative_base(cls=TimestampBase)
