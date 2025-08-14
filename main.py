from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
import pymysql
import hashlib
import os
from datetime import datetime

# 创建FastAPI应用实例
app = FastAPI(title="学生数据平台", description="用户登录验证API", version="1.0.0")

# 导入配置
from config import DB_CONFIG, API_CONFIG

# 定义请求体模型
class LoginRequest(BaseModel):
    username: str
    password: str

# 定义响应模型
class LoginResponse(BaseModel):
    success: bool
    message: str
    user_type: Optional[str] = None
    user_id: Optional[int] = None

def get_db_connection():
    """获取数据库连接"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        return connection
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return None

def hash_password(password: str) -> str:
    """对密码进行哈希处理（简单示例，生产环境建议使用更安全的方法）"""
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
            
            # 验证密码（这里使用简单的哈希比较，生产环境建议使用更安全的方法）
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

@app.post("/login", response_model=LoginResponse)
async def verify_login(login_data: LoginRequest) -> LoginResponse:
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
    """
    try:
        # 验证用户凭据
        user_info = verify_user_credentials(login_data.username, login_data.password)
        
        if user_info:
            return LoginResponse(
                success=True,
                message="登录成功",
                user_type=user_info['user_type'],
                user_id=user_info['id']
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

@app.get("/")
async def root():
    """根路径，返回API信息"""
    return {
        "message": "学生数据平台 - 用户登录验证API", 
        "docs": "/docs",
        "database": "MySQL连接正常" if get_db_connection() else "MySQL连接失败"
    }

@app.get("/health")
async def health_check():
    """健康检查接口"""
    db_status = "正常" if get_db_connection() else "异常"
    return {
        "status": "running",
        "database": db_status,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_CONFIG['host'], port=API_CONFIG['port'])
