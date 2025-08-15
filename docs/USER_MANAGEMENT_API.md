# 用户管理API文档

## 概述

用户管理API提供了完整的用户增删改查功能，支持用户创建、查询、更新、删除和密码重置等操作。

## 基础信息

- **基础URL**: `http://127.0.0.1:8000`
- **API前缀**: `/users`
- **认证方式**: 暂无（可后续添加JWT认证）

## API接口列表

### 1. 创建用户

**POST** `/users/`

创建新用户。

**请求体**:
```json
{
  "username": "new_user",
  "password": "password123",
  "email": "user@example.com",
  "phone": "13800138000",
  "user_type": "student"
}
```

**参数说明**:
- `username` (必填): 用户名，唯一
- `password` (必填): 密码
- `email` (可选): 邮箱地址
- `phone` (可选): 手机号码
- `user_type` (可选): 用户类型，默认为 "student"
  - 可选值: `admin`, `teacher`, `student`

**响应示例**:
```json
{
  "id": 7,
  "username": "new_user",
  "email": "user@example.com",
  "phone": "13800138000",
  "user_type": "student",
  "is_active": true,
  "created_at": "2025-08-15T02:30:00",
  "updated_at": "2025-08-15T02:30:00",
  "last_login": null
}
```

### 2. 获取用户列表

**GET** `/users/`

获取用户列表，支持分页、筛选和搜索。

**查询参数**:
- `page` (可选): 页码，默认为 1
- `page_size` (可选): 每页数量，默认为 10，最大 100
- `user_type` (可选): 用户类型筛选
- `is_active` (可选): 激活状态筛选
- `search` (可选): 搜索关键词（用户名、邮箱、手机号）

**请求示例**:
```
GET /users/?page=1&page_size=10&user_type=student&search=test
```

**响应示例**:
```json
{
  "total": 25,
  "users": [
    {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "phone": "13800138000",
      "user_type": "admin",
      "is_active": true,
      "created_at": "2025-08-14T15:11:58",
      "updated_at": "2025-08-15T02:10:02",
      "last_login": "2025-08-15T02:10:02"
    }
  ],
  "page": 1,
  "page_size": 10
}
```

### 3. 获取单个用户

**GET** `/users/{user_id}`

根据用户ID获取用户详细信息。

**路径参数**:
- `user_id`: 用户ID

**请求示例**:
```
GET /users/1
```

**响应示例**:
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "phone": "13800138000",
  "user_type": "admin",
  "is_active": true,
  "created_at": "2025-08-14T15:11:58",
  "updated_at": "2025-08-15T02:10:02",
  "last_login": "2025-08-15T02:10:02"
}
```

### 4. 更新用户信息

**PUT** `/users/{user_id}`

更新用户信息。

**路径参数**:
- `user_id`: 用户ID

**请求体**:
```json
{
  "email": "new_email@example.com",
  "phone": "13800138099",
  "user_type": "teacher",
  "is_active": true
}
```

**参数说明**:
- 所有字段都是可选的，只更新提供的字段
- `username`: 用户名（需要检查唯一性）
- `email`: 邮箱地址（需要检查唯一性）
- `phone`: 手机号码（需要检查唯一性）
- `user_type`: 用户类型
- `is_active`: 激活状态

**响应示例**:
```json
{
  "id": 1,
  "username": "admin",
  "email": "new_email@example.com",
  "phone": "13800138099",
  "user_type": "teacher",
  "is_active": true,
  "created_at": "2025-08-14T15:11:58",
  "updated_at": "2025-08-15T02:35:00",
  "last_login": "2025-08-15T02:10:02"
}
```

### 5. 删除用户

**DELETE** `/users/{user_id}`

删除用户（软删除，将 `is_active` 设置为 `False`）。

**路径参数**:
- `user_id`: 用户ID

**请求示例**:
```
DELETE /users/7
```

**响应示例**:
```json
{
  "message": "用户 'new_user' 已成功删除",
  "user_id": 7,
  "deleted_at": "2025-08-15T02:40:00"
}
```

### 6. 重置用户密码

**POST** `/users/{user_id}/reset-password`

重置用户密码。

**路径参数**:
- `user_id`: 用户ID

**查询参数**:
- `new_password`: 新密码

**请求示例**:
```
POST /users/1/reset-password?new_password=newpassword123
```

**响应示例**:
```json
{
  "message": "用户 'admin' 密码已重置",
  "user_id": 1,
  "reset_at": "2025-08-15T02:45:00"
}
```

## 错误处理

### 常见错误码

- `400 Bad Request`: 请求参数错误
- `404 Not Found`: 用户不存在
- `500 Internal Server Error`: 服务器内部错误

### 错误响应示例

```json
{
  "detail": "用户名已存在"
}
```

## 使用示例

### Python 示例

```python
import requests

# 创建用户
user_data = {
    "username": "test_user",
    "password": "password123",
    "email": "test@example.com",
    "user_type": "student"
}
response = requests.post("http://127.0.0.1:8000/users/", json=user_data)
user = response.json()

# 获取用户列表
response = requests.get("http://127.0.0.1:8000/users/?page=1&page_size=10")
users = response.json()

# 更新用户
update_data = {"email": "new_email@example.com"}
response = requests.put(f"http://127.0.0.1:8000/users/{user['id']}", json=update_data)

# 删除用户
response = requests.delete(f"http://127.0.0.1:8000/users/{user['id']}")
```

### JavaScript 示例

```javascript
// 创建用户
const userData = {
    username: "test_user",
    password: "password123",
    email: "test@example.com",
    user_type: "student"
};

fetch("http://127.0.0.1:8000/users/", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify(userData)
})
.then(response => response.json())
.then(user => console.log(user));

// 获取用户列表
fetch("http://127.0.0.1:8000/users/?page=1&page_size=10")
.then(response => response.json())
.then(data => console.log(data));
```

## 测试

运行测试脚本：

```bash
python test_user_management.py
```

## 注意事项

1. **密码安全**: 密码使用SHA256哈希存储，生产环境建议使用更安全的算法
2. **软删除**: 删除操作是软删除，用户数据仍然保留在数据库中
3. **唯一性约束**: 用户名、邮箱、手机号都有唯一性检查
4. **分页限制**: 每页最大数量为100
5. **CORS支持**: API已配置CORS，支持跨域请求

## 后续改进

1. 添加JWT认证和授权
2. 实现硬删除功能
3. 添加用户角色和权限管理
4. 实现密码强度验证
5. 添加操作日志记录
