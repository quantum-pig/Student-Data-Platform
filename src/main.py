from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional
import pymysql
import hashlib
import os
from datetime import datetime

# 导入模块 - 使用绝对导入
from user_management import router as user_router
from auth import router as auth_router
from admin_management import router as admin_router

# 创建FastAPI应用实例
app = FastAPI(title="学生数据平台", description="用户登录验证API", version="1.0.0")

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境建议设置具体域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有HTTP头
)

# 导入配置 - 使用绝对导入
from config import DB_CONFIG, API_CONFIG

# 注册路由
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admin_router)

# 基础响应模型
class HealthResponse(BaseModel):
    status: str
    database: str
    timestamp: str

@app.get("/")
async def root():
    """根路径，返回API信息"""
    return {
        "message": "学生数据平台 - 用户登录验证API", 
        "docs": "/docs",
        "database": "MySQL连接正常" if get_db_connection() else "MySQL连接失败"
    }

def get_db_connection():
    """获取数据库连接"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        return connection
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return None

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查接口"""
    db_status = "正常" if get_db_connection() else "异常"
    return HealthResponse(
        status="running",
        database=db_status,
        timestamp=datetime.now().isoformat()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_CONFIG['host'], port=API_CONFIG['port'])
