# 项目结构说明

## 目录组织

```
Student-Data-Platform/
├── src/                    # Python源代码目录
│   ├── main.py            # 主应用入口
│   ├── config.py          # 配置文件
│   ├── auth.py            # 认证模块
│   ├── user_management.py # 用户管理模块
│   ├── test_api.py        # 基础API测试
│   ├── test_auth.py       # 认证API测试
│   ├── test_user_management.py # 用户管理API测试
│   └── verify_passwords.py # 密码验证工具
├── docs/                   # 文档目录
│   ├── README.md          # 项目说明
│   ├── PROJECT_ARCHITECTURE.md # 项目架构
│   ├── USER_MANAGEMENT_API.md # 用户管理API文档
│   ├── DEPLOYMENT.md      # 部署说明
│   ├── PROJECT_STRUCTURE.md # 项目结构说明（本文件）
│   └── test_cors.html     # CORS测试页面
├── sql_scripts/           # 数据库脚本目录
│   ├── create_user_auth_database.sql
│   ├── update_passwords.sql
│   └── README.md
├── website/               # 前端网站目录
│   ├── dist/             # 构建文件
│   ├── src/              # 源代码
│   └── package.json      # 依赖配置
├── run.py                # 项目启动脚本
├── requirements.txt      # Python依赖包
├── .gitignore           # Git忽略文件
└── .venv/               # Python虚拟环境
```

## 目录说明

### 📁 `src/` - Python源代码目录
包含所有Python源代码文件，按功能模块组织：

- **`main.py`** - 主应用入口，负责应用初始化和路由注册
- **`config.py`** - 配置文件，包含数据库连接和API配置
- **`auth.py`** - 认证模块，处理用户登录、登出等认证功能
- **`user_management.py`** - 用户管理模块，提供用户CRUD操作
- **`test_*.py`** - 各种测试脚本，用于验证API功能

### 📁 `docs/` - 文档目录
包含项目相关的所有文档和说明文件：

- **`README.md`** - 项目总体说明
- **`PROJECT_ARCHITECTURE.md`** - 详细的项目架构说明
- **`USER_MANAGEMENT_API.md`** - 用户管理API使用文档
- **`DEPLOYMENT.md`** - 部署和运维指南
- **`PROJECT_STRUCTURE.md`** - 项目结构说明（本文件）
- **`test_cors.html`** - CORS跨域测试页面

### 📁 `sql_scripts/` - 数据库脚本目录
包含数据库相关的SQL脚本：

- **`create_user_auth_database.sql`** - 创建数据库和表的脚本
- **`update_passwords.sql`** - 更新用户密码哈希值的脚本
- **`README.md`** - 数据库脚本使用说明

### 📁 `website/` - 前端网站目录
包含前端相关的文件：

- **`dist/`** - 构建后的静态文件
- **`src/`** - 前端源代码
- **`package.json`** - 前端依赖配置

### 📄 根目录文件
- **`run.py`** - 项目启动脚本，用于启动API服务
- **`requirements.txt`** - Python依赖包列表
- **`.gitignore`** - Git版本控制忽略文件配置

## 文件命名规范

### Python文件
- 使用小写字母和下划线：`user_management.py`
- 测试文件以`test_`开头：`test_auth.py`
- 主文件使用描述性名称：`main.py`, `config.py`

### 文档文件
- 使用大写字母和下划线：`PROJECT_ARCHITECTURE.md`
- 使用描述性名称：`USER_MANAGEMENT_API.md`
- 主要文档使用标准名称：`README.md`

### 目录名称
- 使用小写字母：`src/`, `docs/`, `sql_scripts/`
- 使用描述性名称：`website/`

## 开发工作流

### 1. 启动项目
```bash
# 使用新的启动脚本
python run.py

# 或者直接使用uvicorn
cd src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. 运行测试
```bash
# 运行认证测试
cd src
python test_auth.py

# 运行用户管理测试
python test_user_management.py

# 运行基础API测试
python test_api.py
```

### 3. 查看文档
- API文档：http://127.0.0.1:8000/docs
- 项目文档：查看 `docs/` 目录下的文件

### 4. 数据库操作
```bash
# 创建数据库
mysql -h 119.45.196.184 -u remote_user -p < sql_scripts/create_user_auth_database.sql

# 更新密码
mysql -h 119.45.196.184 -u remote_user -p < sql_scripts/update_passwords.sql
```

## 模块导入说明

由于项目采用了模块化结构，Python文件的导入路径已经进行了相应调整：

### 相对导入
在`src/`目录内的文件使用相对导入：
```python
from .config import DB_CONFIG
from .auth import router as auth_router
```

### 兼容性处理
为了支持不同的运行方式，代码中包含了兼容性处理：
```python
try:
    from .config import DB_CONFIG
except ImportError:
    from config import DB_CONFIG
```

## 扩展建议

### 1. 添加新模块
在`src/`目录下创建新的Python文件，并在`main.py`中注册路由。

### 2. 添加新文档
在`docs/`目录下创建新的Markdown文件，并更新相关索引。

### 3. 添加新测试
在`src/`目录下创建新的测试文件，遵循`test_*.py`命名规范。

### 4. 添加新脚本
在根目录或相应目录下创建新的脚本文件，如数据库迁移脚本等。

## 注意事项

1. **路径依赖**：确保在正确的目录下运行命令
2. **虚拟环境**：始终在虚拟环境中运行项目
3. **导入路径**：注意模块导入路径的正确性
4. **文档同步**：代码变更时及时更新相关文档
5. **测试覆盖**：新功能开发时编写相应的测试
