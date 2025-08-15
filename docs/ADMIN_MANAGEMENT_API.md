# 管理员管理API文档

## 概述

管理员管理API提供了对管理员用户的完整CRUD操作，包括创建、查询、更新、删除和恢复管理员账户。

## 基础信息

- **基础路径**: `/admin`
- **API标签**: 管理员管理
- **认证要求**: 无（可根据需要添加JWT认证）

## API端点

### 1. 创建管理员

**POST** `/admin/`

创建新的管理员账户。

#### 请求参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| username | string | 是 | 用户名（唯一） |
| password | string | 是 | 密码 |
| email | string | 否 | 邮箱地址 |
| phone | string | 否 | 手机号码 |
| real_name | string | 否 | 真实姓名 |
| department | string | 否 | 部门 |
| role_level | string | 否 | 角色级别（admin/super_admin，默认admin） |
| permissions | array | 否 | 权限列表 |

#### 请求示例

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

#### 响应示例

```json
{
  "id": 1,
  "username": "admin_user",
  "email": "admin@example.com",
  "phone": "13800138000",
  "real_name": "管理员姓名",
  "department": "信息技术部",
  "role_level": "admin",
  "permissions": ["user_manage", "system_config"],
  "is_active": true,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00",
  "last_login": null
}
```

### 2. 获取管理员列表

**GET** `/admin/`

获取管理员列表，支持分页和过滤。

#### 查询参数

| 参数名 | 类型 | 默认值 | 描述 |
|--------|------|--------|------|
| page | integer | 1 | 页码 |
| page_size | integer | 10 | 每页数量（最大100） |
| role_level | string | - | 角色级别过滤 |
| department | string | - | 部门过滤 |
| is_active | boolean | - | 活跃状态过滤 |

#### 请求示例

```bash
GET /admin/?page=1&page_size=10&role_level=admin&is_active=true
```

#### 响应示例

```json
{
  "total": 5,
  "admins": [
    {
      "id": 1,
      "username": "admin_user",
      "email": "admin@example.com",
      "phone": "13800138000",
      "real_name": "管理员姓名",
      "department": "信息技术部",
      "role_level": "admin",
      "permissions": ["user_manage", "system_config"],
      "is_active": true,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00",
      "last_login": "2024-01-01T12:00:00"
    }
  ],
  "page": 1,
  "page_size": 10
}
```

### 3. 获取特定管理员

**GET** `/admin/{admin_id}`

获取特定管理员的详细信息。

#### 路径参数

| 参数名 | 类型 | 描述 |
|--------|------|------|
| admin_id | integer | 管理员ID |

#### 请求示例

```bash
GET /admin/1
```

#### 响应示例

```json
{
  "id": 1,
  "username": "admin_user",
  "email": "admin@example.com",
  "phone": "13800138000",
  "real_name": "管理员姓名",
  "department": "信息技术部",
  "role_level": "admin",
  "permissions": ["user_manage", "system_config"],
  "is_active": true,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00",
  "last_login": "2024-01-01T12:00:00"
}
```

### 4. 更新管理员信息

**PUT** `/admin/{admin_id}`

更新管理员的基本信息。

#### 路径参数

| 参数名 | 类型 | 描述 |
|--------|------|------|
| admin_id | integer | 管理员ID |

#### 请求参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| username | string | 否 | 用户名 |
| email | string | 否 | 邮箱地址 |
| phone | string | 否 | 手机号码 |
| real_name | string | 否 | 真实姓名 |
| department | string | 否 | 部门 |
| role_level | string | 否 | 角色级别 |
| permissions | array | 否 | 权限列表 |
| is_active | boolean | 否 | 活跃状态 |

#### 请求示例

```json
{
  "real_name": "更新后的管理员姓名",
  "department": "系统管理部",
  "role_level": "super_admin",
  "permissions": ["user_manage", "system_config", "admin_manage"]
}
```

### 5. 更新管理员密码

**PUT** `/admin/{admin_id}/password`

更新管理员的密码。

#### 路径参数

| 参数名 | 类型 | 描述 |
|--------|------|------|
| admin_id | integer | 管理员ID |

#### 请求参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| old_password | string | 是 | 旧密码 |
| new_password | string | 是 | 新密码 |

#### 请求示例

```json
{
  "old_password": "admin123",
  "new_password": "newadmin123"
}
```

#### 响应示例

```json
{
  "message": "密码更新成功"
}
```

### 6. 删除管理员

**DELETE** `/admin/{admin_id}`

删除管理员（软删除，将is_active设置为false）。

#### 路径参数

| 参数名 | 类型 | 描述 |
|--------|------|------|
| admin_id | integer | 管理员ID |

#### 请求示例

```bash
DELETE /admin/1
```

#### 响应示例

```json
{
  "message": "管理员删除成功"
}
```

### 7. 恢复管理员

**POST** `/admin/{admin_id}/restore`

恢复被删除的管理员（将is_active设置为true）。

#### 路径参数

| 参数名 | 类型 | 描述 |
|--------|------|------|
| admin_id | integer | 管理员ID |

#### 请求示例

```bash
POST /admin/1/restore
```

#### 响应示例

```json
{
  "message": "管理员恢复成功"
}
```

## 数据模型

### AdminCreate

```python
class AdminCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    phone: Optional[str] = None
    real_name: Optional[str] = None
    department: Optional[str] = None
    role_level: str = "admin"
    permissions: Optional[List[str]] = None
```

### AdminUpdate

```python
class AdminUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    real_name: Optional[str] = None
    department: Optional[str] = None
    role_level: Optional[str] = None
    permissions: Optional[List[str]] = None
    is_active: Optional[bool] = None
```

### AdminResponse

```python
class AdminResponse(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    phone: Optional[str] = None
    real_name: Optional[str] = None
    department: Optional[str] = None
    role_level: str
    permissions: Optional[List[str]] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
```

## 错误处理

### 常见错误码

| 状态码 | 描述 |
|--------|------|
| 400 | 请求参数错误（如用户名已存在、邮箱已存在等） |
| 404 | 管理员不存在 |
| 500 | 服务器内部错误 |

### 错误响应示例

```json
{
  "detail": "用户名已存在"
}
```

## 使用示例

### cURL示例

#### 创建管理员

```bash
curl -X POST "http://localhost:8000/admin/" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "new_admin",
       "password": "admin123",
       "email": "newadmin@example.com",
       "real_name": "新管理员",
       "department": "信息技术部",
       "role_level": "admin",
       "permissions": ["user_manage", "system_config"]
     }'
```

#### 获取管理员列表

```bash
curl "http://localhost:8000/admin/?page=1&page_size=10&role_level=admin"
```

#### 更新管理员信息

```bash
curl -X PUT "http://localhost:8000/admin/1" \
     -H "Content-Type: application/json" \
     -d '{
       "real_name": "更新后的管理员",
       "department": "系统管理部",
       "role_level": "super_admin"
     }'
```

#### 更新密码

```bash
curl -X PUT "http://localhost:8000/admin/1/password" \
     -H "Content-Type: application/json" \
     -d '{
       "old_password": "admin123",
       "new_password": "newadmin123"
     }'
```

## 注意事项

1. **密码安全**: 所有密码都使用SHA256进行哈希处理
2. **软删除**: 删除操作是软删除，不会真正删除数据
3. **权限管理**: 权限以逗号分隔的字符串形式存储
4. **唯一性约束**: 用户名和邮箱地址必须唯一
5. **角色级别**: 支持admin和super_admin两种角色级别

## 测试

可以使用提供的测试文件 `test_admin_management.py` 来验证API功能：

```bash
python3 src/test_admin_management.py
```
