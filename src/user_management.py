#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户管理API模块
实现用户的增删改查功能
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import pymysql
from datetime import datetime
import hashlib
try:
    from .config import DB_CONFIG
except ImportError:
    from config import DB_CONFIG

# 创建路由器
router = APIRouter(prefix="/users", tags=["用户管理"])

# 数据模型定义
class UserCreate(BaseModel):
    """创建用户请求模型"""
    username: str
    password: str
    email: Optional[str] = None
    phone: Optional[str] = None
    user_type: str = "student"  # 默认为学生

class UserUpdate(BaseModel):
    """更新用户请求模型"""
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    user_type: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(BaseModel):
    """用户响应模型"""
    id: int
    username: str
    email: Optional[str] = None
    phone: Optional[str] = None
    user_type: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

class UserListResponse(BaseModel):
    """用户列表响应模型"""
    total: int
    users: List[UserResponse]
    page: int
    page_size: int

def get_db_connection():
    """获取数据库连接"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        return connection
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return None

def hash_password(password: str) -> str:
    """对密码进行哈希处理"""
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/", response_model=UserResponse, summary="创建新用户")
async def create_user(user_data: UserCreate):
    """
    创建新用户
    
    - **username**: 用户名（必填，唯一）
    - **password**: 密码（必填）
    - **email**: 邮箱地址（可选）
    - **phone**: 手机号码（可选）
    - **user_type**: 用户类型（admin/teacher/student，默认为student）
    """
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="数据库连接失败")
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # 检查用户名是否已存在
            check_sql = "SELECT id FROM users WHERE username = %s"
            cursor.execute(check_sql, (user_data.username,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="用户名已存在")
            
            # 检查邮箱是否已存在（如果提供）
            if user_data.email:
                check_email_sql = "SELECT id FROM users WHERE email = %s"
                cursor.execute(check_email_sql, (user_data.email,))
                if cursor.fetchone():
                    raise HTTPException(status_code=400, detail="邮箱地址已存在")
            
            # 检查手机号是否已存在（如果提供）
            if user_data.phone:
                check_phone_sql = "SELECT id FROM users WHERE phone = %s"
                cursor.execute(check_phone_sql, (user_data.phone,))
                if cursor.fetchone():
                    raise HTTPException(status_code=400, detail="手机号码已存在")
            
            # 验证用户类型
            valid_types = ["admin", "teacher", "student"]
            if user_data.user_type not in valid_types:
                raise HTTPException(status_code=400, detail=f"用户类型必须是: {', '.join(valid_types)}")
            
            # 创建用户
            insert_sql = """
                INSERT INTO users (username, password, email, phone, user_type, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            now = datetime.now()
            hashed_password = hash_password(user_data.password)
            
            cursor.execute(insert_sql, (
                user_data.username,
                hashed_password,
                user_data.email,
                user_data.phone,
                user_data.user_type,
                now,
                now
            ))
            
            user_id = cursor.lastrowid
            
            # 获取创建的用户信息
            select_sql = "SELECT * FROM users WHERE id = %s"
            cursor.execute(select_sql, (user_id,))
            user = cursor.fetchone()
            
            return UserResponse(**user)
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"创建用户时出错: {e}")
        raise HTTPException(status_code=500, detail="创建用户失败")
    finally:
        connection.close()

@router.get("/", response_model=UserListResponse, summary="获取用户列表")
async def get_users(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    user_type: Optional[str] = Query(None, description="用户类型筛选"),
    is_active: Optional[bool] = Query(None, description="激活状态筛选"),
    search: Optional[str] = Query(None, description="搜索关键词（用户名、邮箱、手机号）")
):
    """
    获取用户列表，支持分页、筛选和搜索
    
    - **page**: 页码（从1开始）
    - **page_size**: 每页数量（1-100）
    - **user_type**: 用户类型筛选（admin/teacher/student）
    - **is_active**: 激活状态筛选（true/false）
    - **search**: 搜索关键词
    """
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="数据库连接失败")
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # 构建查询条件
            where_conditions = []
            params = []
            
            if user_type:
                where_conditions.append("user_type = %s")
                params.append(user_type)
            
            if is_active is not None:
                where_conditions.append("is_active = %s")
                params.append(is_active)
            
            if search:
                where_conditions.append("(username LIKE %s OR email LIKE %s OR phone LIKE %s)")
                search_param = f"%{search}%"
                params.extend([search_param, search_param, search_param])
            
            where_clause = " WHERE " + " AND ".join(where_conditions) if where_conditions else ""
            
            # 获取总数
            count_sql = f"SELECT COUNT(*) as total FROM users{where_clause}"
            cursor.execute(count_sql, params)
            total = cursor.fetchone()['total']
            
            # 获取用户列表
            offset = (page - 1) * page_size
            select_sql = f"""
                SELECT id, username, email, phone, user_type, is_active, 
                       created_at, updated_at, last_login
                FROM users{where_clause}
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
            """
            cursor.execute(select_sql, params + [page_size, offset])
            users = cursor.fetchall()
            
            return UserListResponse(
                total=total,
                users=[UserResponse(**user) for user in users],
                page=page,
                page_size=page_size
            )
            
    except Exception as e:
        print(f"获取用户列表时出错: {e}")
        raise HTTPException(status_code=500, detail="获取用户列表失败")
    finally:
        connection.close()

@router.get("/{user_id}", response_model=UserResponse, summary="获取单个用户")
async def get_user(user_id: int):
    """
    根据用户ID获取用户详细信息
    
    - **user_id**: 用户ID
    """
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="数据库连接失败")
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            select_sql = """
                SELECT id, username, email, phone, user_type, is_active, 
                       created_at, updated_at, last_login
                FROM users WHERE id = %s
            """
            cursor.execute(select_sql, (user_id,))
            user = cursor.fetchone()
            
            if not user:
                raise HTTPException(status_code=404, detail="用户不存在")
            
            return UserResponse(**user)
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"获取用户时出错: {e}")
        raise HTTPException(status_code=500, detail="获取用户失败")
    finally:
        connection.close()

@router.put("/{user_id}", response_model=UserResponse, summary="更新用户信息")
async def update_user(user_id: int, user_data: UserUpdate):
    """
    更新用户信息
    
    - **user_id**: 用户ID
    - **user_data**: 要更新的用户信息
    """
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="数据库连接失败")
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # 检查用户是否存在
            check_sql = "SELECT id FROM users WHERE id = %s"
            cursor.execute(check_sql, (user_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="用户不存在")
            
            # 构建更新字段
            update_fields = []
            params = []
            
            if user_data.username is not None:
                # 检查用户名是否已被其他用户使用
                check_username_sql = "SELECT id FROM users WHERE username = %s AND id != %s"
                cursor.execute(check_username_sql, (user_data.username, user_id))
                if cursor.fetchone():
                    raise HTTPException(status_code=400, detail="用户名已被其他用户使用")
                update_fields.append("username = %s")
                params.append(user_data.username)
            
            if user_data.email is not None:
                # 检查邮箱是否已被其他用户使用
                check_email_sql = "SELECT id FROM users WHERE email = %s AND id != %s"
                cursor.execute(check_email_sql, (user_data.email, user_id))
                if cursor.fetchone():
                    raise HTTPException(status_code=400, detail="邮箱地址已被其他用户使用")
                update_fields.append("email = %s")
                params.append(user_data.email)
            
            if user_data.phone is not None:
                # 检查手机号是否已被其他用户使用
                check_phone_sql = "SELECT id FROM users WHERE phone = %s AND id != %s"
                cursor.execute(check_phone_sql, (user_data.phone, user_id))
                if cursor.fetchone():
                    raise HTTPException(status_code=400, detail="手机号码已被其他用户使用")
                update_fields.append("phone = %s")
                params.append(user_data.phone)
            
            if user_data.user_type is not None:
                valid_types = ["admin", "teacher", "student"]
                if user_data.user_type not in valid_types:
                    raise HTTPException(status_code=400, detail=f"用户类型必须是: {', '.join(valid_types)}")
                update_fields.append("user_type = %s")
                params.append(user_data.user_type)
            
            if user_data.is_active is not None:
                update_fields.append("is_active = %s")
                params.append(user_data.is_active)
            
            if not update_fields:
                raise HTTPException(status_code=400, detail="没有提供要更新的字段")
            
            # 添加更新时间
            update_fields.append("updated_at = %s")
            params.append(datetime.now())
            params.append(user_id)
            
            # 执行更新
            update_sql = f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s"
            cursor.execute(update_sql, params)
            
            # 获取更新后的用户信息
            select_sql = """
                SELECT id, username, email, phone, user_type, is_active, 
                       created_at, updated_at, last_login
                FROM users WHERE id = %s
            """
            cursor.execute(select_sql, (user_id,))
            user = cursor.fetchone()
            
            return UserResponse(**user)
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"更新用户时出错: {e}")
        raise HTTPException(status_code=500, detail="更新用户失败")
    finally:
        connection.close()

@router.delete("/{user_id}", summary="删除用户")
async def delete_user(user_id: int):
    """
    删除用户（软删除，将is_active设置为False）
    
    - **user_id**: 用户ID
    """
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="数据库连接失败")
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # 检查用户是否存在
            check_sql = "SELECT id, username FROM users WHERE id = %s"
            cursor.execute(check_sql, (user_id,))
            user = cursor.fetchone()
            
            if not user:
                raise HTTPException(status_code=404, detail="用户不存在")
            
            # 软删除：将is_active设置为False
            update_sql = "UPDATE users SET is_active = FALSE, updated_at = %s WHERE id = %s"
            cursor.execute(update_sql, (datetime.now(), user_id))
            
            return {
                "message": f"用户 '{user['username']}' 已成功删除",
                "user_id": user_id,
                "deleted_at": datetime.now().isoformat()
            }
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"删除用户时出错: {e}")
        raise HTTPException(status_code=500, detail="删除用户失败")
    finally:
        connection.close()

@router.post("/{user_id}/reset-password", summary="重置用户密码")
async def reset_user_password(user_id: int, new_password: str):
    """
    重置用户密码
    
    - **user_id**: 用户ID
    - **new_password**: 新密码
    """
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="数据库连接失败")
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # 检查用户是否存在
            check_sql = "SELECT id, username FROM users WHERE id = %s"
            cursor.execute(check_sql, (user_id,))
            user = cursor.fetchone()
            
            if not user:
                raise HTTPException(status_code=404, detail="用户不存在")
            
            # 更新密码
            hashed_password = hash_password(new_password)
            update_sql = "UPDATE users SET password = %s, updated_at = %s WHERE id = %s"
            cursor.execute(update_sql, (hashed_password, datetime.now(), user_id))
            
            return {
                "message": f"用户 '{user['username']}' 密码已重置",
                "user_id": user_id,
                "reset_at": datetime.now().isoformat()
            }
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"重置密码时出错: {e}")
        raise HTTPException(status_code=500, detail="重置密码失败")
    finally:
        connection.close()
