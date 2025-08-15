# 学生数据平台 - 用户登录验证API

这是一个使用FastAPI构建的完整学生数据平台API，提供用户认证、用户管理等功能。

## 功能特性

- 🔐 **用户认证系统**
  - 用户登录验证
  - 密码哈希加密
  - 登录日志记录
  - 会话管理

- 👥 **用户管理**
  - 用户注册和创建
  - 用户信息更新
  - 用户查询和列表
  - 用户状态管理

- 🗄️ **数据库集成**
  - MySQL数据库连接
  - 用户数据持久化
  - 数据库健康检查

- 🌐 **API特性**
  - RESTful API设计
  - CORS跨域支持
  - 自动API文档生成
  - 健康检查端点

## 技术栈

- **后端框架**: FastAPI
- **数据库**: MySQL
- **Python版本**: 3.8+
- **依赖管理**: requirements.txt

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行应用

### 方式一：使用启动脚本（推荐）

```bash
python run.py
```

### 方式二：直接运行主文件

```bash
cd src
python main.py
```

### 方式三：使用uvicorn

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## API文档

启动服务后，您可以访问以下地址：

- **Swagger UI文档**: http://localhost:8000/docs
- **ReDoc文档**: http://localhost:8000/redoc
- **健康检查**: http://localhost:8000/health

## API端点

### 认证相关 (`/auth`)

#### POST /auth/login
用户登录验证

**请求体：**
```json
{
  "username": "用户名",
  "password": "密码"
}
```

**响应：**
```json
{
  "success": true,
  "message": "登录成功",
  "user_type": "student",
  "user_id": 1,
  "token": null
}
```

#### POST /auth/logout
用户登出

**请求体：**
```json
{
  "user_id": 1,
  "token": "可选的令牌"
}
```

### 用户管理 (`/users`)

#### POST /users/
创建新用户

**请求体：**
```json
{
  "username": "新用户名",
  "password": "密码",
  "email": "邮箱@example.com",
  "phone": "13800138000",
  "user_type": "student"
}
```

#### GET /users/
获取用户列表（支持分页）

**查询参数：**
- `page`: 页码（默认1）
- `page_size`: 每页数量（默认10）
- `user_type`: 用户类型过滤
- `is_active`: 活跃状态过滤

#### GET /users/{user_id}
获取特定用户信息

#### PUT /users/{user_id}
更新用户信息

#### DELETE /users/{user_id}
删除用户（软删除）

### 管理员管理 (`/admin`)

#### POST /admin/
创建新管理员

**请求体：**
```json
{
  "username": "admin_user",
  "password": "admin123",
  "email": "admin@example.com",
  "phone": "13800138000",
  "real_name": "管理员姓名",
  "department": "信息技术部",
  "role_level": "admin",
  "permissions": ["user_manage", "system_config"]
}
```

#### GET /admin/
获取管理员列表（支持分页和过滤）

**查询参数：**
- `page`: 页码（默认1）
- `page_size`: 每页数量（默认10，最大100）
- `role_level`: 角色级别过滤（admin/super_admin）
- `department`: 部门过滤
- `is_active`: 活跃状态过滤

#### GET /admin/{admin_id}
获取特定管理员信息

#### PUT /admin/{admin_id}
更新管理员信息

#### PUT /admin/{admin_id}/password
更新管理员密码

**请求体：**
```json
{
  "old_password": "旧密码",
  "new_password": "新密码"
}
```

#### DELETE /admin/{admin_id}
删除管理员（软删除）

#### POST /admin/{admin_id}/restore
恢复被删除的管理员

### 系统相关

#### GET /
根路径，返回API信息

#### GET /health
健康检查接口

## 示例请求

### 用户登录
```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "test_user", "password": "password123"}'
```

### 创建用户
```bash
curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "new_user",
       "password": "password123",
       "email": "user@example.com",
       "user_type": "student"
     }'
```

### 获取用户列表
```bash
curl "http://localhost:8000/users/?page=1&page_size=10"
```

### 创建管理员
```bash
curl -X POST "http://localhost:8000/admin/" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "admin_user",
       "password": "admin123",
       "email": "admin@example.com",
       "real_name": "管理员姓名",
       "department": "信息技术部",
       "role_level": "admin",
       "permissions": ["user_manage", "system_config"]
     }'
```

### 获取管理员列表
```bash
curl "http://localhost:8000/admin/?page=1&page_size=10&role_level=admin"
```

### 更新管理员密码
```bash
curl -X PUT "http://localhost:8000/admin/1/password" \
     -H "Content-Type: application/json" \
     -d '{
       "old_password": "admin123",
       "new_password": "newadmin123"
     }'
```

## 项目结构

```
Student-Data-Platform/
├── src/                    # 源代码目录
│   ├── __init__.py        # 包初始化文件
│   ├── main.py            # FastAPI应用主文件
│   ├── config.py          # 配置文件
│   ├── auth.py            # 认证模块
│   ├── user_management.py # 用户管理模块
│   ├── admin_management.py # 管理员管理模块
│   └── test_*.py          # 测试文件
├── docs/                  # 文档目录
│   ├── README.md          # 项目说明文档
│   ├── PROJECT_STRUCTURE.md
│   ├── PROJECT_ARCHITECTURE.md
│   └── USER_MANAGEMENT_API.md
├── website/               # 前端网站
├── sql_scripts/           # 数据库脚本
├── requirements.txt       # Python依赖包
└── run.py                # 项目启动脚本
```

## 配置说明

项目配置位于 `src/config.py`：

- **数据库配置**: MySQL连接参数
- **API配置**: 服务地址和端口
- **安全配置**: 密码哈希算法等

## 开发说明

- 项目使用模块化设计，便于维护和扩展
- 所有API端点都有完整的错误处理
- 支持CORS跨域请求
- 包含完整的测试文件

## 许可证

本项目仅供学习和研究使用。
