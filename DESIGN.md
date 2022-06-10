# 前言

本项目使用了两种设计模式，分别为[`DDD(Domain-Driven Design)`](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf)和[`CQRS(Command and Query Responsibility Segregation)`](https://docs.microsoft.com/en-us/azure/architecture/patterns/cqrs)

但由于实际需求并不需要设计一个大型系统，故本项目只借用了两种设计模式中的部分设计

# 涉及概念

## Entity

在 DDD 中 Entity 要求具备唯一的`标识`，通过 Python 自带的 `dataclass`可以非常快地创建一个实体，由于 dataclass 默认实现了 `__eq__()`接口，所以只要是属于 dataclass 的类，都是充血模型，满足 Entity 的定义。例如：

```python
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
```

## VO(Value Object)

VO具备几个特点：

- 与 Entity 绑定，不会单独存在
- 同 Entity 一起创建，一起销毁，具有一样的生命周期
- 不可修改性(immutable)

本项目中的邮箱字段就是一个典型的`VO`，虽然基础类型 str 完全可以满足对邮箱的存储需求，但这类字段通常会有固定的格式和校验需求。例如：

```python
@dataclass(init=False, eq=True, frozen=True)
class Email:
    """
    Email Value Object
    """

    value: str

    def __init__(self, value: str):
        try:
            email_validator.validate_email(value, check_deliverability=False)
        except email_validator.EmailNotValidError as e:
            raise ValueError(f"邮箱格式不正确: {e}")
        else:
            object.__setattr__(self, "value", value)
```

当 dataclass 的 frozen 为 True 时，此时的对象就是不可修改的，满足 VO 的定义下。

## DO(Data Object)

DO 存在的目的是为了和数据库物理表格进行一一映射，不能含有业务逻辑。例如：

```python
class CommentDO(Base):
    """
    Comment DO
    """

    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    content = Column(Text(200), nullable=False)
    parent_id = Column(Integer, ForeignKey("comment.id"))
    children = relationship("CommentDTO")
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow())
    updated_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"CommentDO(id={self.id!r}, content={self.content!r}, parent_id={self.parent_id!r})"

    def to_entity(self) -> Comment:
        return Comment(
            id=self.id,
            content=self.content,
            parent_id=self.parent_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @staticmethod
    def from_entity(comment: Comment) -> "CommentDO":
        return CommentDO(
            id=comment.id,
            content=comment.content,
            parent_id=comment.parent_id,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )
```

DO 可以通过`to_entity`和`from_entity`与 Entity 进行转换。

## DTO(Data Transfer Object)

主要作为 Application 层的入参和出参，比如 CQRS 里的Command、Query、Event，以及Request、Response等都属于DTO的范畴。DTO的价值在于适配不同的业务场景的入参和出参，避免让业务对象变成一个万能大对象。例如：

```python
class CommentCreateDTO(BaseModel):
    """
    Comment Create Data Transfer Object
    """

    content: str = Field(min_length=3, max_length=200, example="测试评论")
    parent_id: Optional[int] = Field(example=3)
```

## Repository

Repository 相比传统的 DAO 直接关联某个数据库进行操作，Repository 具有几个特点：

- 通常需要先写接口再实现，接口命名不应该出现底层相关的特征，例如将select、insert、update、delete替换成find、save、remove
- Repository 操作的是 Entity 对象，不应该操作 DO
- Repository 接口在 Domain 层，实现在 Infrastructure 层

Repository 接口例子如下：

```python
class CommentBaseRepository(ABC):
    """
    Comment Repository 接口
    """

    @abstractmethod
    def find(self, comment_id: int) -> Optional[Comment]:
        raise NotImplementedError

    @abstractmethod
    def save(self, comment: Comment) -> Optional[Comment]:
        raise NotImplementedError

    @abstractmethod
    def remove(self, comment_id: int):
        raise NotImplementedError
```

Repository 实现例子如下：

```python
class CommentRepository(CommentBaseRepository):
    """
    Comment Repository 实现
    """

    def __init__(self, session: Session):
        self.session: Session = session

    def find(self, comment_id: int) -> Optional[Comment]:
        try:
            comment_do: CommentDO = self.session.query(CommentDO).filter_by(id=comment_id).one()
        except NoResultFound:
            return None
        else:
            return comment_do.to_entity()

    def save(self, comment: Comment) -> Optional[Comment]:
        if not comment.id:
            # Create
            comment_do = CommentDO.from_entity(comment)
            try:
                self.session.add(comment_do)
            except:
                self.session.rollback()
                raise
            else:
                self.session.commit()
                return comment_do.to_entity()
        else:
            # Update
            pass

    def remove(self, comment_id: int):
        try:
            comment_do: CommentDO = self.session.query(CommentDO).filter_by(id=comment_id).one()
        except NoResultFound:
            return None
        else:
            self.session.delete(comment_do)
            self.session.commit()
```

