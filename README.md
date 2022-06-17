# 前言

## 介绍
本项目是本人在面某远程工作岗位所接到的笔试题，笔试题本身没有什么难度，但我结合 [`DDD(Domain-Driven Design)`](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf)和[`CQRS(Command and Query Responsibility Segregation)`](https://docs.microsoft.com/en-us/azure/architecture/patterns/cqrs) 这两种设计模式对这个项目进行了编写，最终落地了 DDD 的部分概念，详情可以参考[设计文档](https://github.com/mago960806/comments-tree/blob/main/DESIGN.md)

# 笔试题

## 题目标题
评论树

## 题目内容

使用Python+数据库，做一个简单的“树形留言”网站。难点可能在“无限层级”，由于可以无限嵌套，在数据库设计、ORM/SQL查询、以及页面展示上都需要一定经验。同时也需要考察候选人基本的用户注册/登录功能，主要是对用户密码的处理、字段的验证、浏览器 session/cookie 的应用等技能。由于现在前后端分离已经是常态，要求 Python 后端提供RESTFul API，前端页面可以使用任一种前端 JS 框架（包含但不限于jquery/react/vue/angular等）

## 功能需求

- 用户可以在网站上注册
  - 需要填写 username, password, email。
  - username需要检查：不可为空，只能使用字母和数字，长度在5~20之间，不能与已有用户名重复
  - password需要检查：不可为空，长度在8~20之间，至少包含一个大写、一个小写、一个数字、一个特殊符号
  - email需要检查：不可为空，格式要正确，不能与已有email重复。为简单起见，不需要发送邮件确认

- 用户可以在网站上登录
  - 使用username+password，或者email+password 登录
  - 提供”remember me”功能，登录后一个月内不需要重新登录
  - 如果未勾选”remember me”，则关闭浏览器后再次访问会提示注册或登录
  - 用户登录后，需要在页面上方显示用户名和Email

- 用户登录后，可以发表留言。
  - 留言长度在3~200字之间，可以为中文
  - 输入时会动态提示还可以再输入多少字
  - 会记录留言发表时间

- 可以针对某个留言进行再次评论
  - 评论输入的要求与留言相同
  - 可以针对某个评论再次评论，不限层级

- 用户可以查看留言
  - 只需要一个页面显示全部留言及树形嵌套的评论即可（一次性加载，不要懒加载）
  - 留言以时间倒序从上向下排列，最上面是最新的
  - 某个留言旁边可以看到发布者用户名和发表时间
  - 查看留言时不需要登录

## 技术需求

- 提供一条命令进行网站的初始化、启动等功能，最终可以在浏览器中自动打开网站首页
- Python的 Web 框架使用 Flask 或 FastAPI
- 使用数据库（关系数据库或NoSQL），自行建表，使用SQL/NO-SQL/ORM等。为了Review方便，推荐使用较简单的文件式数据库（如sqlite等），不需要安装
- 用户注册时，密码保存到数据库里不能使用明文，需要某种形式的不可逆加密。
- 可以使用 ORM 或者原生 SQL 等方式进行数据库查询
- 后端提供的 RESTFul API，需要考虑到权限检查，以及正确的HTTP Method和HTTP Status Code
- 对于较大层数的嵌套留言（超过50层），不会出现明显的性能问题
- 有恰当的单元测试
