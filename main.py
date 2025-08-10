from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

# 创建FastAPI应用实例
app = FastAPI(title="学生数据平台", description="用户登录验证API", version="1.0.0")

# 定义请求体模型
class LoginRequest(BaseModel):
    username: str
    password: str

# 定义响应模型
class LoginResponse(BaseModel):
    success: bool

@app.post("/login", response_model=LoginResponse)
async def verify_login(login_data: LoginRequest) -> LoginResponse:
    """
    用户登录验证API
    
    参数:
    - username: 用户名 (字符串)
    - password: 密码 (字符串)
    
    返回:
    - success: 始终返回True (布尔值)
    """
    # 无论输入什么参数，都返回True
    return LoginResponse(success=True)

@app.get("/")
async def root():
    """根路径，返回API信息"""
    return {"message": "学生数据平台 - 用户登录验证API", "docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
