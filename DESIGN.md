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
    created_by: str
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
    Comment Data Object
    """

    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    content = Column(Text(200), nullable=False)
    parent_id = Column(Integer, ForeignKey("comment.id"), nullable=True)
    children = relationship("CommentDO")
    created_by = Column(String(200), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow())
    updated_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"CommentDO(id={self.id!r}, content={self.content!r}, parent_id={self.parent_id!r})"

    def to_entity(self) -> Comment:
        """
        DO 转换成 Entity
        """
        return Comment(
            id=self.id,
            content=self.content,
            parent_id=self.parent_id,
            created_by=self.created_by,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @staticmethod
    def from_entity(comment: Comment) -> "CommentDO":
        """
        Entity 转换成 DO
        """
        return CommentDO(
            id=comment.id,
            content=comment.content,
            parent_id=comment.parent_id,
            created_by=comment.created_by,
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
    created_by: Optional[str] = "匿名用户"
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

    def find_all(self) -> List[Comment]:
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

    def find_all(self) -> List[CommentTreeNode]:
        comment_dos: List[CommentDO] = (
            self.session.query(CommentDO).filter_by(parent_id=None).order_by(CommentDO.created_at)
        )
        return get_comments_tree(comment_dos)

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

## UseCase

UseCase 分两类，一类为 QueryUseCase，一类为 CommandUseCase，分别对应读操作和写操作的封装。

UseCase 中接受 Repository 对象作为参数，将上层所需的业务场景都在此实现。例如：

```python
class CommentCommandUseCase(object):
    def __init__(self, repository: "CommentRepository"):
        self.repository = repository

    def create_comment(self, data: CommentCreateDTO) -> Optional[CommentReadDTO]:
        comment = Comment(content=data.content, parent_id=data.parent_id, created_by=data.created_by)
        created_comment = self.repository.save(comment)
        return CommentReadDTO.from_entity(created_comment)

    def delete_comment(self, comment_id: int):
        self.repository.remove(comment_id)
```

# 项目架构

```
.
├── DESIGN.md # 设计文档
├── README.md # 说明文档
├── app # 项目主目录
│   ├── __init__.py
│   ├── config.py 
│   ├── domain # 域对象层(Domain Layer), 包含 Entity 对象, VO 对象, Exception 对象, Repository 接口
│   │   ├── __init__.py
│   │   ├── comment
│   │   │   ├── __init__.py
│   │   │   ├── entity.py
│   │   │   ├── exception.py
│   │   │   └── repository.py
│   │   └── user
│   │       ├── __init__.py
│   │       ├── entity.py
│   │       ├── exception.py
│   │       ├── repository.py
│   │       └── vo.py
│   ├── infrastructure # 基础架构层(Infrastructure Layer), 包含 DO 对象 和 Repository 实现
│   │   ├── __init__.py
│   │   ├── comment
│   │   │   ├── __init__.py
│   │   │   ├── do.py
│   │   │   └── repository.py
│   │   ├── database.py # SQLalchemy ORM 封装
│   │   └── user
│   │       ├── __init__.py
│   │       ├── do.py
│   │       └── repository.py
│   ├── routers # 路由层(Router Layer), 包含所有 API 接口对应的 Handler 函数
│   │   ├── __init__.py
│   │   ├── comment.py
│   │   └── user.py
│   ├── tests # 单元测试
│   │   ├── __init__.py
│   │   ├── conftest.py # pytest 配置
│   │   ├── routers
│   │   │   ├── __init__.py
│   │   │   ├── test_comment.py
│   │   │   └── test_user.py
│   │   ├── setup_test_db.py # 初始化测试数据库
│   │   ├── usecase
│   │   │   ├── __init__.py
│   │   │   └── dto
│   │   │       ├── __init__.py
│   │   │       └── test_command.py
│   │   └── utils
│   │       ├── __init__.py
│   │       └── test_auth.py
│   ├── usecase # 用例层(UseCase Layer), 包含各类 DTO 和 UseCase 对象, 例如 Command, Query
│   │   ├── __init__.py
│   │   ├── comment
│   │   │   ├── __init__.py
│   │   │   ├── dto
│   │   │   │   ├── __init__.py
│   │   │   │   ├── command.py
│   │   │   │   └── query.py
│   │   │   └── usecase
│   │   │       ├── __init__.py
│   │   │       ├── command.py
│   │   │       └── query.py
│   │   └── user
│   │       ├── __init__.py
│   │       ├── dto
│   │       │   ├── __init__.py
│   │       │   ├── command.py
│   │       │   └── query.py
│   │       └── usecase
│   │           ├── __init__.py
│   │           ├── command.py
│   │           └── query.py
│   └── utils # 工具函数
│       ├── __init__.py
│       └── auth.py # 认证相关函数
├── init_db.py # 数据库初始化脚本
├── poetry.lock # 依赖版本管理文件
├── pyproject.toml # 项目信息文件
├── requirements.txt # 项目依赖
├── server.py # 程序入口
```

## 其他说明

### 初次使用

1. 创建虚拟环境：python3 -m venv venv

2. 激活虚拟环境：source venv/bin/activate
3. 安装依赖：pip install -r requirements.txt
4. 创建配置文件：touch .env
5. 写入以下配置：

```ini
# DEBUG 模式
DEBUG=true
SQL_DEBUG=false

# 监听端口
SERVER_HOST=127.0.0.1
SERVER_PORT=8000

# 数据库配置
DATABASE_URI=sqlite:///sqlite3.db

# 认证配置
SECRET_KEY=e8aac33715c3a12ebb831a943ced8459e295bde9b965a9283c34143c158b6c56
ACCESS_TOKEN_EXPIRE_MINUTES=43200
```

6. 运行数据库初始化脚本：python init_db.py
7. 启动项目：python server.py
8. 打开浏览器访问：http://127.0.0.1:8000/web/ 

###  开发

启动开发模式, 可通过执行`python server.py`。

然后访问 http://127.0.0.1:8000/web/ 即可访问到前端。

### 接口文档

在项目运行后可访问 http://127.0.0.1:8000/docs 获取基于 OpenAPI 的接口文档。

### 测试

本项目使用 pytest 作为单元测试框架，启动测试只需要执行`pytest`即可
