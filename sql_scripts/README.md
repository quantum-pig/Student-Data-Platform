# MySQL 数据库脚本说明

## 概述
这个文件夹包含了用于学生数据平台的MySQL数据库脚本，主要用于用户登录验证功能。

## 文件说明

### `create_user_auth_database.sql`
用户登录验证数据库创建脚本，包含以下功能：

1. **创建数据库**: `user_auth_db`
   - 使用UTF8MB4字符集，支持完整的Unicode字符
   - 使用InnoDB存储引擎

2. **用户表 (users)**:
   - `id`: 用户ID，自增主键
   - `username`: 用户名，唯一约束
   - `password`: 密码字段（建议使用加密存储）
   - `email`: 邮箱地址，可选
   - `phone`: 手机号码，可选
   - `user_type`: 用户类型（teacher/student/admin），默认为student
   - `created_at`: 创建时间
   - `updated_at`: 更新时间
   - `is_active`: 账户激活状态
   - `last_login`: 最后登录时间

3. **登录日志表 (login_logs)**:
   - 记录用户登录历史
   - 包含登录时间、IP地址、用户代理等信息
   - 支持成功/失败状态记录

## 使用方法

### 1. 通过命令行执行
```bash
mysql -u your_username -p < create_user_auth_database.sql
```

### 2. 通过MySQL客户端执行
```sql
source /path/to/create_user_auth_database.sql;
```

### 3. 分步执行
```sql
-- 创建数据库
CREATE DATABASE IF NOT EXISTS user_auth_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE user_auth_db;

-- 然后执行表创建语句...
```

## 用户类型说明

数据库支持三种用户类型：

1. **管理员 (admin)**: 系统管理员，拥有最高权限
2. **教师 (teacher)**: 教师用户，可以管理学生数据和课程信息
3. **学生 (student)**: 学生用户，默认用户类型，可以查看自己的数据

用户类型使用ENUM类型存储，确保数据的一致性和完整性。

## 安全建议

1. **密码加密**: 在实际应用中，请务必对密码进行加密存储（如使用bcrypt、Argon2等）
2. **索引优化**: 已为常用查询字段添加了索引
3. **字符集**: 使用UTF8MB4支持完整的Unicode字符集
4. **外键约束**: 登录日志表与用户表建立了外键关系
5. **权限控制**: 根据用户类型实现不同的权限控制策略

## 示例数据
脚本中包含了六种不同用户类型的示例用户：

### 管理员用户
- admin/admin123 (admin@example.com)

### 教师用户
- teacher_zhang/teacher123 (zhang@school.com)
- teacher_li/teacher456 (li@school.com)

### 学生用户
- student_wang/student123 (wang@student.com)
- student_liu/student456 (liu@student.com)
- student_chen/student789 (chen@student.com)

**注意**: 这些仅用于测试，生产环境中请删除或修改这些示例数据。

## 数据库连接信息
- 数据库名: `user_auth_db`
- 字符集: `utf8mb4`
- 排序规则: `utf8mb4_unicode_ci`
