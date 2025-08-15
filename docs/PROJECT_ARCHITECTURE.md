# 学生数据平台 - 项目架构说明

## 项目概述

学生数据平台是一个基于FastAPI的现代化Web API系统，采用模块化架构设计，支持用户认证、用户管理等功能。

## 技术栈

- **后端框架**: FastAPI (Python)
- **数据库**: MySQL
- **ORM**: PyMySQL (原生SQL)
- **认证**: 自定义认证系统（预留JWT接口）
- **文档**: Swagger UI / ReDoc
- **部署**: Uvicorn

## 项目结构

```
Student-Data-Platform/
├── main.py                     # 主应用入口
├── config.py                   # 配置文件
├── auth.py                     # 认证模块
├── user_management.py          # 用户管理模块
├── requirements.txt            # 依赖包列表
├── test_api.py                 # 基础API测试
├── test_auth.py                # 认证API测试
├── test_user_management.py     # 用户管理API测试
├── test_cors.html              # CORS测试页面
├── verify_passwords.py         # 密码验证工具
├── PROJECT_ARCHITECTURE.md     # 项目架构文档
├── USER_MANAGEMENT_API.md      # 用户管理API文档
├── DEPLOYMENT.md               # 部署说明
└── sql_scripts/                # 数据库脚本
    ├── create_user_auth_database.sql
    ├── update_passwords.sql
    └── README.md
```

## 模块架构

### 1. 主应用模块 (`main.py`)

**职责**:
- 应用初始化和配置
- 中间件配置（CORS等）
- 路由注册
- 基础健康检查接口

**主要功能**:
- FastAPI应用实例创建
- CORS中间件配置
- 模块路由注册
- 系统健康检查

### 2. 认证模块 (`auth.py`)

**职责**:
- 用户登录验证
- 用户登出处理
- 用户状态验证
- 用户资料获取

**API接口**:
- `POST /auth/login` - 用户登录
- `POST /auth/logout` - 用户登出
- `GET /auth/verify` - 验证用户状态
- `GET /auth/profile/{user_id}` - 获取用户资料

**未来扩展**:
- JWT令牌生成和验证
- 令牌刷新机制
- 会话管理

### 3. 用户管理模块 (`user_management.py`)

**职责**:
- 用户CRUD操作
- 用户列表查询
- 密码重置
- 用户状态管理

**API接口**:
- `POST /users/` - 创建用户
- `GET /users/` - 获取用户列表
- `GET /users/{user_id}` - 获取单个用户
- `PUT /users/{user_id}` - 更新用户
- `DELETE /users/{user_id}` - 删除用户
- `POST /users/{user_id}/reset-password` - 重置密码

### 4. 配置模块 (`config.py`)

**职责**:
- 数据库连接配置
- API服务配置
- 安全配置

**配置项**:
- 数据库连接参数
- API服务参数
- 安全策略配置

## 数据库设计

### 用户表 (`users`)
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    user_type ENUM('teacher', 'student', 'admin') NOT NULL DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP NULL
);
```

### 登录日志表 (`login_logs`)
```sql
CREATE TABLE login_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    login_ip VARCHAR(45),
    user_agent TEXT,
    login_status ENUM('success', 'failed') NOT NULL,
    failure_reason VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);
```

## API架构

### 路由结构
```
/api/v1/
├── /auth/          # 认证相关
│   ├── /login
│   ├── /logout
│   ├── /verify
│   └── /profile/{user_id}
├── /users/         # 用户管理
│   ├── /
│   ├── /{user_id}
│   └── /{user_id}/reset-password
└── /health         # 系统健康检查
```

### 响应格式
所有API响应都遵循统一的JSON格式：

**成功响应**:
```json
{
  "success": true,
  "message": "操作成功",
  "data": {...}
}
```

**错误响应**:
```json
{
  "success": false,
  "message": "错误信息",
  "detail": "详细错误描述"
}
```

## 安全设计

### 1. 密码安全
- 使用SHA256哈希算法
- 预留更安全算法接口（bcrypt等）
- 密码重置功能

### 2. 数据验证
- 输入参数验证
- SQL注入防护
- 唯一性约束检查

### 3. 访问控制
- 用户类型权限控制
- 软删除机制
- 登录日志记录

### 4. CORS配置
- 支持跨域请求
- 可配置允许的域名
- 支持预检请求

## 扩展性设计

### 1. 模块化架构
- 功能模块独立
- 易于添加新功能
- 清晰的职责分离

### 2. 配置管理
- 环境变量支持
- 配置文件分离
- 灵活的配置项

### 3. 数据库设计
- 标准化表结构
- 索引优化
- 外键约束

### 4. API设计
- RESTful风格
- 版本控制支持
- 统一的响应格式

## 开发规范

### 1. 代码规范
- PEP 8 Python代码规范
- 类型注解
- 文档字符串

### 2. 错误处理
- 统一的异常处理
- 详细的错误信息
- 日志记录

### 3. 测试规范
- 单元测试
- 集成测试
- API测试

## 部署架构

### 开发环境
```bash
# 启动开发服务器
python main.py

# 或使用uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 生产环境
```bash
# 使用gunicorn + uvicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 未来规划

### 短期目标
1. 添加JWT认证
2. 实现用户权限管理
3. 添加API限流
4. 完善错误处理

### 中期目标
1. 添加缓存层（Redis）
2. 实现微服务架构
3. 添加监控和日志
4. 实现自动化部署

### 长期目标
1. 支持多租户
2. 实现分布式架构
3. 添加AI功能
4. 移动端支持

## 维护指南

### 日常维护
1. 数据库备份
2. 日志清理
3. 性能监控
4. 安全更新

### 故障处理
1. 服务重启
2. 数据库连接检查
3. 日志分析
4. 性能调优

## 贡献指南

### 开发流程
1. 功能分支开发
2. 代码审查
3. 测试验证
4. 合并发布

### 代码提交
- 清晰的提交信息
- 功能完整性
- 测试覆盖
- 文档更新
