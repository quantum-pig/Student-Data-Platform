#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
认证模块
包含用户登录验证和相关认证功能
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
import pymysql
import hashlib
import os
from datetime import datetime
try:
    from .config import DB_CONFIG
except ImportError:
    from config import DB_CONFIG

# 创建路由器
router = APIRouter(prefix="/auth", tags=["认证"])

# 数据模型定义
class LoginRequest(BaseModel):
    """登录请求模型"""
    username: str
    password: str

class LoginResponse(BaseModel):
    """登录响应模型"""
    success: bool
    message: str
    user_type: Optional[str] = None
    user_id: Optional[int] = None
    token: Optional[str] = None  # 为未来JWT实现预留

class LogoutRequest(BaseModel):
    """登出请求模型"""
    user_id: int
    token: Optional[str] = None

class LogoutResponse(BaseModel):
    """登出响应模型"""
    success: bool
    message: str

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

def verify_user_credentials(username: str, password: str) -> Optional[Dict]:
    """验证用户凭据"""
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # 查询用户信息
            sql = """
                SELECT id, username, password, user_type, is_active 
                FROM users 
                WHERE username = %s AND is_active = TRUE
            """
            cursor.execute(sql, (username,))
            user = cursor.fetchone()
            
            if not user:
                return None
            
            # 验证密码
            hashed_password = hash_password(password)
            if hashed_password == user['password']:
                # 更新最后登录时间
                update_sql = "UPDATE users SET last_login = %s WHERE id = %s"
                cursor.execute(update_sql, (datetime.now(), user['id']))
                
                # 记录登录日志
                log_sql = """
                    INSERT INTO login_logs (user_id, login_ip, user_agent, login_status) 
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(log_sql, (user['id'], '127.0.0.1', 'API Client', 'success'))
                
                return {
                    'id': user['id'],
                    'username': user['username'],
                    'user_type': user['user_type']
                }
            
            # 记录失败的登录尝试
            if user:
                log_sql = """
                    INSERT INTO login_logs (user_id, login_ip, user_agent, login_status, failure_reason) 
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(log_sql, (user['id'], '127.0.0.1', 'API Client', 'failed', '密码错误'))
            
            return None
            
    except Exception as e:
        print(f"验证用户凭据时出错: {e}")
        return None
    finally:
        connection.close()

@router.post("/login", response_model=LoginResponse, summary="用户登录")
async def login(login_data: LoginRequest) -> LoginResponse:
    """
    用户登录验证API
    
    参数:
    - username: 用户名 (字符串)
    - password: 密码 (字符串)
    
    返回:
    - success: 验证结果 (布尔值)
    - message: 响应消息 (字符串)
    - user_type: 用户类型 (可选)
    - user_id: 用户ID (可选)
    - token: 认证令牌 (可选，为未来JWT实现预留)
    """
    try:
        # 验证用户凭据
        user_info = verify_user_credentials(login_data.username, login_data.password)
        
        if user_info:
            return LoginResponse(
                success=True,
                message="登录成功",
                user_type=user_info['user_type'],
                user_id=user_info['id'],
                token=None  # 未来可返回JWT token
            )
        else:
            return LoginResponse(
                success=False,
                message="用户名或密码错误"
            )
            
    except Exception as e:
        print(f"登录验证过程中出错: {e}")
        return LoginResponse(
            success=False,
            message="服务器内部错误，请稍后重试"
        )

@router.post("/logout", response_model=LogoutResponse, summary="用户登出")
async def logout(logout_data: LogoutRequest) -> LogoutResponse:
    """
    用户登出API
    
    参数:
    - user_id: 用户ID (整数)
    - token: 认证令牌 (可选)
    
    返回:
    - success: 登出结果 (布尔值)
    - message: 响应消息 (字符串)
    """
    try:
        # 这里可以添加token验证逻辑
        # 目前只是简单的响应，未来可以实现token失效等逻辑
        
        return LogoutResponse(
            success=True,
            message="登出成功"
        )
        
    except Exception as e:
        print(f"登出过程中出错: {e}")
        return LogoutResponse(
            success=False,
            message="登出失败，请稍后重试"
        )

@router.get("/verify", summary="验证用户状态")
async def verify_user_status(user_id: int):
    """
    验证用户状态API
    
    参数:
    - user_id: 用户ID (整数)
    
    返回:
    - 用户状态信息
    """
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="数据库连接失败")
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                SELECT id, username, user_type, is_active, last_login
                FROM users 
                WHERE id = %s
            """
            cursor.execute(sql, (user_id,))
            user = cursor.fetchone()
            
            if not user:
                raise HTTPException(status_code=404, detail="用户不存在")
            
            return {
                "user_id": user['id'],
                "username": user['username'],
                "user_type": user['user_type'],
                "is_active": user['is_active'],
                "last_login": user['last_login'],
                "status": "active" if user['is_active'] else "inactive"
            }
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"验证用户状态时出错: {e}")
        raise HTTPException(status_code=500, detail="验证用户状态失败")
    finally:
        connection.close()

@router.get("/profile/{user_id}", summary="获取用户资料")
async def get_user_profile(user_id: int):
    """
    获取用户资料API
    
    参数:
    - user_id: 用户ID (整数)
    
    返回:
    - 用户资料信息
    """
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="数据库连接失败")
    
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                SELECT id, username, email, phone, user_type, is_active, 
                       created_at, updated_at, last_login
                FROM users 
                WHERE id = %s
            """
            cursor.execute(sql, (user_id,))
            user = cursor.fetchone()
            
            if not user:
                raise HTTPException(status_code=404, detail="用户不存在")
            
            return {
                "id": user['id'],
                "username": user['username'],
                "email": user['email'],
                "phone": user['phone'],
                "user_type": user['user_type'],
                "is_active": user['is_active'],
                "created_at": user['created_at'],
                "updated_at": user['updated_at'],
                "last_login": user['last_login']
            }
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"获取用户资料时出错: {e}")
        raise HTTPException(status_code=500, detail="获取用户资料失败")
    finally:
        connection.close()

# 为未来扩展预留的函数
def generate_jwt_token(user_info: Dict) -> str:
    """生成JWT令牌（未来实现）"""
    # TODO: 实现JWT token生成
    pass

def verify_jwt_token(token: str) -> Optional[Dict]:
    """验证JWT令牌（未来实现）"""
    # TODO: 实现JWT token验证
    pass

def refresh_token(token: str) -> str:
    """刷新JWT令牌（未来实现）"""
    # TODO: 实现token刷新
    pass
