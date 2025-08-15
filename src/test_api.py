#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API测试脚本
用于测试用户登录验证功能
"""

import requests
import json
from typing import Dict

# API基础URL
BASE_URL = "http://127.0.0.1:8000"

# 添加当前目录到Python路径
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

def test_health_check():
    """测试健康检查接口"""
    print("=== 测试健康检查接口 ===")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"健康检查失败: {e}")
        return False

def test_login(username: str, password: str, expected_success: bool = True):
    """测试登录接口"""
    print(f"\n=== 测试登录: {username} ===")
    
    login_data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            if result['success'] == expected_success:
                print("✅ 测试通过")
                return True
            else:
                print("❌ 测试失败 - 结果不符合预期")
                return False
        else:
            print(f"❌ 请求失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

def main():
    """主测试函数"""
    print("开始API测试...")
    
    # 测试健康检查
    if not test_health_check():
        print("健康检查失败，请确保API服务正在运行")
        return
    
    # 测试正确的用户名和密码
    print("\n" + "="*50)
    print("测试正确的用户名和密码:")
    
    test_cases = [
        ("admin", "admin123", True),
        ("teacher_zhang", "teacher123", True),
        ("teacher_li", "teacher456", True),
        ("student_wang", "student123", True),
        ("student_liu", "student456", True),
        ("student_chen", "student789", True),
    ]
    
    success_count = 0
    for username, password, expected in test_cases:
        if test_login(username, password, expected):
            success_count += 1
    
    # 测试错误的用户名和密码
    print("\n" + "="*50)
    print("测试错误的用户名和密码:")
    
    error_cases = [
        ("admin", "wrong_password", False),
        ("nonexistent_user", "any_password", False),
        ("", "", False),
    ]
    
    for username, password, expected in error_cases:
        if test_login(username, password, expected):
            success_count += 1
    
    # 测试结果统计
    total_tests = len(test_cases) + len(error_cases)
    print(f"\n" + "="*50)
    print(f"测试完成: {success_count}/{total_tests} 通过")
    
    if success_count == total_tests:
        print("🎉 所有测试通过！")
    else:
        print("⚠️  部分测试失败，请检查API和数据库配置")

if __name__ == "__main__":
    main()
