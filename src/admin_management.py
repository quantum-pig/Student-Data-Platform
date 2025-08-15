#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
管理员管理API模块
实现管理员用户的增删改查功能
"""

from fastapi import APIRouter, HTTPException, Query, Depends
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
router = APIRouter(prefix="/admin", tags=["管理员管理"])

# 数据模型定义
class AdminCreate(BaseModel):
    """创建管理员请求模型"""
    username: str
    password: str
    email: Optional[str] = None
    phone: Optional[str] = None
    real_name: Optional[str] = None
    department: Optional[str] = None
    role_level: str = "admin"  # admin, super_admin
    permissions: Optional[List[str]] = None

class AdminUpdate(BaseModel):
    """更新管理员请求模型"""
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    real_name: Optional[str] = None
    department: Optional[str] = None
    role_level: Optional[str] = None
    permissions: Optional[List[str]] = None
    is_active: Optional[bool] = None

class AdminResponse(BaseModel):
    """管理员响应模型"""
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

class AdminListResponse(BaseModel):
    """管理员列表响应模型"""
    total: int
    admins: List[AdminResponse]
    page: int
    page_size: int

class AdminPasswordUpdate(BaseModel):
    """管理员密码更新模型"""
    old_password: str
    new_password: str

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

def verify_admin_exists(admin_id: int) -> bool:
    """验证管理员是否存在且为管理员类型"""
    connection = get_db_connection()
    if not connection:
        return False
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT id FROM users WHERE id = %s AND user_type = 'admin'"
            cursor.execute(sql, (admin_id,))
            return cursor.fetchone() is not None
    except Exception as e:
        print(f"验证管理员失败: {e}")
        return False
    finally:
        connection.close()

@router.post("/", response_model=AdminResponse, summary="创建新管理员")
async def create_admin(admin_data: AdminCreate):
    """
    创建新管理员
    
    - **username**: 用户名（必填，唯一）
    - **password**: 密码（必填）
    - **email**: 邮箱地址（可选）
    - **phone**: 手机号码（可选）
    - **real_name**: 真实姓名（可选）
    - **department**: 部门（可选）
    - **role_level**: 角色级别（admin/super_admin，默认为admin）
    - **permissions**: 权限列表（可选）
    """
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="数据库连接失败")
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # 检查用户名是否已存在
            check_sql = "SELECT id FROM users WHERE username = %s"
            cursor.execute(check_sql, (admin_data.username,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="用户名已存在")
            
            # 检查邮箱是否已存在（如果提供）
            if admin_data.email:
                check_email_sql = "SELECT id FROM users WHERE email = %s"
                cursor.execute(check_email_sql, (admin_data.email,))
                if cursor.fetchone():
                    raise HTTPException(status_code=400, detail="邮箱地址已存在")
            
            # 创建管理员用户
            hashed_password = hash_password(admin_data.password)
            permissions_str = ",".join(admin_data.permissions) if admin_data.permissions else ""
            
            insert_sql = """
                INSERT INTO users (username, password, email, phone, user_type, 
                                 real_name, department, role_level, permissions, 
                                 is_active, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_sql, (
                admin_data.username,
                hashed_password,
                admin_data.email,
                admin_data.phone,
                'admin',  # 固定为admin类型
                admin_data.real_name,
                admin_data.department,
                admin_data.role_level,
                permissions_str,
                True,
                datetime.now(),
                datetime.now()
            ))
            
            admin_id = cursor.lastrowid
            connection.commit()
            
            # 返回创建的管理员信息
            return AdminResponse(
                id=admin_id,
                username=admin_data.username,
                email=admin_data.email,
                phone=admin_data.phone,
                real_name=admin_data.real_name,
                department=admin_data.department,
                role_level=admin_data.role_level,
                permissions=admin_data.permissions,
                is_active=True,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
    except HTTPException:
        raise
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"创建管理员失败: {str(e)}")
    finally:
        connection.close()

@router.get("/", response_model=AdminListResponse, summary="获取管理员列表")
async def get_admins(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    role_level: Optional[str] = Query(None, description="角色级别过滤"),
    department: Optional[str] = Query(None, description="部门过滤"),
    is_active: Optional[bool] = Query(None, description="活跃状态过滤")
):
    """
    获取管理员列表，支持分页和过滤
    
    - **page**: 页码（默认1）
    - **page_size**: 每页数量（默认10，最大100）
    - **role_level**: 角色级别过滤
    - **department**: 部门过滤
    - **is_active**: 活跃状态过滤
    """
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="数据库连接失败")
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # 构建查询条件
            where_conditions = ["user_type = 'admin'"]
            params = []
            
            if role_level:
                where_conditions.append("role_level = %s")
                params.append(role_level)
            
            if department:
                where_conditions.append("department = %s")
                params.append(department)
            
            if is_active is not None:
                where_conditions.append("is_active = %s")
                params.append(is_active)
            
            where_clause = " AND ".join(where_conditions)
            
            # 获取总数
            count_sql = f"SELECT COUNT(*) as total FROM users WHERE {where_clause}"
            cursor.execute(count_sql, params)
            total = cursor.fetchone()['total']
            
            # 获取分页数据
            offset = (page - 1) * page_size
            select_sql = f"""
                SELECT id, username, email, phone, real_name, department, 
                       role_level, permissions, is_active, created_at, 
                       updated_at, last_login
                FROM users 
                WHERE {where_clause}
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
            """
            cursor.execute(select_sql, params + [page_size, offset])
            admins = cursor.fetchall()
            
            # 处理权限字段
            admin_list = []
            for admin in admins:
                permissions = admin['permissions'].split(',') if admin['permissions'] else []
                admin_list.append(AdminResponse(
                    id=admin['id'],
                    username=admin['username'],
                    email=admin['email'],
                    phone=admin['phone'],
                    real_name=admin['real_name'],
                    department=admin['department'],
                    role_level=admin['role_level'],
                    permissions=permissions,
                    is_active=admin['is_active'],
                    created_at=admin['created_at'],
                    updated_at=admin['updated_at'],
                    last_login=admin['last_login']
                ))
            
            return AdminListResponse(
                total=total,
                admins=admin_list,
                page=page,
                page_size=page_size
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取管理员列表失败: {str(e)}")
    finally:
        connection.close()

@router.get("/{admin_id}", response_model=AdminResponse, summary="获取特定管理员信息")
async def get_admin(admin_id: int):
    """
    获取特定管理员的详细信息
    
    - **admin_id**: 管理员ID
    """
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="数据库连接失败")
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                SELECT id, username, email, phone, real_name, department, 
                       role_level, permissions, is_active, created_at, 
                       updated_at, last_login
                FROM users 
                WHERE id = %s AND user_type = 'admin'
            """
            cursor.execute(sql, (admin_id,))
            admin = cursor.fetchone()
            
            if not admin:
                raise HTTPException(status_code=404, detail="管理员不存在")
            
            permissions = admin['permissions'].split(',') if admin['permissions'] else []
            
            return AdminResponse(
                id=admin['id'],
                username=admin['username'],
                email=admin['email'],
                phone=admin['phone'],
                real_name=admin['real_name'],
                department=admin['department'],
                role_level=admin['role_level'],
                permissions=permissions,
                is_active=admin['is_active'],
                created_at=admin['created_at'],
                updated_at=admin['updated_at'],
                last_login=admin['last_login']
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取管理员信息失败: {str(e)}")
    finally:
        connection.close()

@router.put("/{admin_id}", response_model=AdminResponse, summary="更新管理员信息")
async def update_admin(admin_id: int, admin_data: AdminUpdate):
    """
    更新管理员信息
    
    - **admin_id**: 管理员ID
    - **admin_data**: 更新的管理员信息
    """
    # 验证管理员是否存在
    if not verify_admin_exists(admin_id):
        raise HTTPException(status_code=404, detail="管理员不存在")
    
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="数据库连接失败")
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # 构建更新字段
            update_fields = []
            params = []
            
            if admin_data.username is not None:
                # 检查用户名是否已被其他用户使用
                check_sql = "SELECT id FROM users WHERE username = %s AND id != %s"
                cursor.execute(check_sql, (admin_data.username, admin_id))
                if cursor.fetchone():
                    raise HTTPException(status_code=400, detail="用户名已被使用")
                update_fields.append("username = %s")
                params.append(admin_data.username)
            
            if admin_data.email is not None:
                # 检查邮箱是否已被其他用户使用
                check_sql = "SELECT id FROM users WHERE email = %s AND id != %s"
                cursor.execute(check_sql, (admin_data.email, admin_id))
                if cursor.fetchone():
                    raise HTTPException(status_code=400, detail="邮箱已被使用")
                update_fields.append("email = %s")
                params.append(admin_data.email)
            
            if admin_data.phone is not None:
                update_fields.append("phone = %s")
                params.append(admin_data.phone)
            
            if admin_data.real_name is not None:
                update_fields.append("real_name = %s")
                params.append(admin_data.real_name)
            
            if admin_data.department is not None:
                update_fields.append("department = %s")
                params.append(admin_data.department)
            
            if admin_data.role_level is not None:
                update_fields.append("role_level = %s")
                params.append(admin_data.role_level)
            
            if admin_data.permissions is not None:
                permissions_str = ",".join(admin_data.permissions)
                update_fields.append("permissions = %s")
                params.append(permissions_str)
            
            if admin_data.is_active is not None:
                update_fields.append("is_active = %s")
                params.append(admin_data.is_active)
            
            if not update_fields:
                raise HTTPException(status_code=400, detail="没有提供要更新的字段")
            
            update_fields.append("updated_at = %s")
            params.append(datetime.now())
            params.append(admin_id)
            
            # 执行更新
            update_sql = f"""
                UPDATE users 
                SET {', '.join(update_fields)}
                WHERE id = %s AND user_type = 'admin'
            """
            cursor.execute(update_sql, params)
            
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="管理员不存在或更新失败")
            
            connection.commit()
            
            # 返回更新后的信息
            return await get_admin(admin_id)
            
    except HTTPException:
        raise
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"更新管理员失败: {str(e)}")
    finally:
        connection.close()

@router.put("/{admin_id}/password", summary="更新管理员密码")
async def update_admin_password(admin_id: int, password_data: AdminPasswordUpdate):
    """
    更新管理员密码
    
    - **admin_id**: 管理员ID
    - **password_data**: 密码更新数据
    """
    # 验证管理员是否存在
    if not verify_admin_exists(admin_id):
        raise HTTPException(status_code=404, detail="管理员不存在")
    
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="数据库连接失败")
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # 验证旧密码
            sql = "SELECT password FROM users WHERE id = %s AND user_type = 'admin'"
            cursor.execute(sql, (admin_id,))
            admin = cursor.fetchone()
            
            if not admin:
                raise HTTPException(status_code=404, detail="管理员不存在")
            
            old_hashed_password = hash_password(password_data.old_password)
            if old_hashed_password != admin['password']:
                raise HTTPException(status_code=400, detail="旧密码不正确")
            
            # 更新密码
            new_hashed_password = hash_password(password_data.new_password)
            update_sql = """
                UPDATE users 
                SET password = %s, updated_at = %s
                WHERE id = %s AND user_type = 'admin'
            """
            cursor.execute(update_sql, (new_hashed_password, datetime.now(), admin_id))
            
            connection.commit()
            
            return {"message": "密码更新成功"}
            
    except HTTPException:
        raise
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"更新密码失败: {str(e)}")
    finally:
        connection.close()

@router.delete("/{admin_id}", summary="删除管理员")
async def delete_admin(admin_id: int):
    """
    删除管理员（软删除）
    
    - **admin_id**: 管理员ID
    """
    # 验证管理员是否存在
    if not verify_admin_exists(admin_id):
        raise HTTPException(status_code=404, detail="管理员不存在")
    
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="数据库连接失败")
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # 软删除：将is_active设置为False
            sql = """
                UPDATE users 
                SET is_active = FALSE, updated_at = %s
                WHERE id = %s AND user_type = 'admin'
            """
            cursor.execute(sql, (datetime.now(), admin_id))
            
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="管理员不存在或删除失败")
            
            connection.commit()
            
            return {"message": "管理员删除成功"}
            
    except HTTPException:
        raise
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"删除管理员失败: {str(e)}")
    finally:
        connection.close()

@router.post("/{admin_id}/restore", summary="恢复管理员")
async def restore_admin(admin_id: int):
    """
    恢复被删除的管理员
    
    - **admin_id**: 管理员ID
    """
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="数据库连接失败")
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # 检查管理员是否存在（包括已删除的）
            sql = "SELECT id FROM users WHERE id = %s AND user_type = 'admin'"
            cursor.execute(sql, (admin_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="管理员不存在")
            
            # 恢复管理员
            restore_sql = """
                UPDATE users 
                SET is_active = TRUE, updated_at = %s
                WHERE id = %s AND user_type = 'admin'
            """
            cursor.execute(restore_sql, (datetime.now(), admin_id))
            
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="管理员不存在或恢复失败")
            
            connection.commit()
            
            return {"message": "管理员恢复成功"}
            
    except HTTPException:
        raise
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"恢复管理员失败: {str(e)}")
    finally:
        connection.close()
