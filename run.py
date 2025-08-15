#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目启动脚本
用于启动学生数据平台API服务
"""

import sys
import os

# 添加src目录到Python路径
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

# 设置环境变量，告诉Python这是作为脚本运行
os.environ['PYTHONPATH'] = src_path

try:
    # 导入配置
    from src.config import API_CONFIG
    
    # 导入主应用
    from src.main import app
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print(f"📁 当前工作目录: {os.getcwd()}")
    print(f"📁 src目录路径: {src_path}")
    print(f"📁 Python路径: {sys.path}")
    sys.exit(1)

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 启动学生数据平台API服务...")
    print(f"📍 服务地址: http://{API_CONFIG['host']}:{API_CONFIG['port']}")
    print(f"📚 API文档: http://{API_CONFIG['host']}:{API_CONFIG['port']}/docs")
    print("=" * 50)
    
    # 切换到src目录运行
    original_cwd = os.getcwd()
    os.chdir(src_path)
    
    try:
        uvicorn.run(
            "src.main:app",
            host=API_CONFIG['host'],
            port=API_CONFIG['port'],
            reload=True,
            log_level="info"
        )
    finally:
        # 恢复原始工作目录
        os.chdir(original_cwd)
