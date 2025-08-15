# 学生数据平台 - 部署说明

## 概述
这是一个基于FastAPI的用户登录验证系统，使用MySQL数据库存储用户信息。

## 系统要求
- Python 3.8+
- MySQL 5.7+
- 网络连接到数据库服务器 (119.45.196.184)

## 安装步骤

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置数据库
1. 修改 `config.py` 文件中的数据库连接信息：
   ```python
   DB_CONFIG = {
       'host': '119.45.196.184',
       'port': 3306,
       'user': 'your_username',  # 修改为实际的数据库用户名
       'password': 'your_password',  # 修改为实际的数据库密码
       'database': 'user_auth_db',
       'charset': 'utf8mb4',
       'autocommit': True
   }
   ```

### 3. 创建数据库
在MySQL中执行以下脚本：
```bash
mysql -h 119.45.196.184 -u your_username -p < sql_scripts/create_user_auth_database.sql
```

### 4. 更新密码哈希
执行密码更新脚本：
```bash
mysql -h 119.45.196.184 -u your_username -p < sql_scripts/update_passwords.sql
```

## 运行应用

### 开发环境
```bash
python main.py
```

### 生产环境
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API接口

### 1. 健康检查
- **GET** `/health`
- 返回系统状态和数据库连接状态

### 2. 用户登录
- **POST** `/login`
- 请求体：
  ```json
  {
    "username": "admin",
    "password": "admin123"
  }
  ```
- 响应：
  ```json
  {
    "success": true,
    "message": "登录成功",
    "user_type": "admin",
    "user_id": 1
  }
  ```

## 测试

### 运行测试脚本
```bash
python test_api.py
```

### 测试用户账号
- 管理员: `admin` / `admin123`
- 教师: `teacher_zhang` / `teacher123`
- 学生: `student_wang` / `student123`

## 安全注意事项

1. **密码安全**: 生产环境中请使用更强的密码哈希算法（如bcrypt）
2. **数据库安全**: 确保数据库连接使用SSL/TLS加密
3. **API安全**: 考虑添加JWT令牌认证
4. **环境变量**: 敏感信息应通过环境变量配置

## 故障排除

### 数据库连接失败
1. 检查数据库服务器是否可访问
2. 验证用户名和密码是否正确
3. 确认数据库是否存在

### API启动失败
1. 检查端口是否被占用
2. 确认所有依赖已正确安装
3. 查看错误日志

## 监控和日志

- API访问日志可通过FastAPI的日志系统查看
- 数据库连接状态可通过 `/health` 接口监控
- 登录日志存储在 `login_logs` 表中
