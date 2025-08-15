#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
认证API测试脚本
用于测试认证相关的功能
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

def test_login():
    """测试登录功能"""
    print("=== 测试登录功能 ===")
    
    # 测试正确的用户名和密码
    test_cases = [
        ("admin", "admin123", True),
        ("teacher_zhang", "teacher123", True),
        ("student_wang", "student123", True),
        ("admin", "wrong_password", False),
        ("nonexistent_user", "any_password", False),
    ]
    
    success_count = 0
    for username, password, expected in test_cases:
        print(f"\n测试: {username} / {password}")
        
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
                
                if result['success'] == expected:
                    print("✅ 测试通过")
                    success_count += 1
                else:
                    print("❌ 测试失败 - 结果不符合预期")
            else:
                print(f"❌ 请求失败: {response.text}")
                
        except Exception as e:
            print(f"❌ 测试异常: {e}")
    
    print(f"\n登录测试完成: {success_count}/{len(test_cases)} 通过")
    return success_count == len(test_cases)

def test_logout():
    """测试登出功能"""
    print("\n=== 测试登出功能 ===")
    
    logout_data = {
        "user_id": 1,
        "token": "test_token"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/logout", json=logout_data)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            if result['success']:
                print("✅ 登出测试通过")
                return True
            else:
                print("❌ 登出测试失败")
                return False
        else:
            print(f"❌ 请求失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

def test_verify_user_status():
    """测试用户状态验证"""
    print("\n=== 测试用户状态验证 ===")
    
    # 测试存在的用户
    try:
        response = requests.get(f"{BASE_URL}/auth/verify?user_id=1")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
            print("✅ 用户状态验证测试通过")
        else:
            print(f"❌ 请求失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False
    
    # 测试不存在的用户
    try:
        response = requests.get(f"{BASE_URL}/auth/verify?user_id=999")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 404:
            print("✅ 不存在用户验证测试通过")
            return True
        else:
            print(f"❌ 预期404错误，但得到: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

def test_get_user_profile():
    """测试获取用户资料"""
    print("\n=== 测试获取用户资料 ===")
    
    # 测试存在的用户
    try:
        response = requests.get(f"{BASE_URL}/auth/profile/1")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
            print("✅ 获取用户资料测试通过")
        else:
            print(f"❌ 请求失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False
    
    # 测试不存在的用户
    try:
        response = requests.get(f"{BASE_URL}/auth/profile/999")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 404:
            print("✅ 不存在用户资料获取测试通过")
            return True
        else:
            print(f"❌ 预期404错误，但得到: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

def main():
    """主测试函数"""
    print("开始认证API测试...")
    print("=" * 60)
    
    test_results = []
    
    # 1. 测试登录
    test_results.append(test_login())
    
    # 2. 测试登出
    test_results.append(test_logout())
    
    # 3. 测试用户状态验证
    test_results.append(test_verify_user_status())
    
    # 4. 测试获取用户资料
    test_results.append(test_get_user_profile())
    
    # 统计结果
    passed_tests = sum(test_results)
    total_tests = len(test_results)
    
    print("\n" + "=" * 60)
    print(f"认证API测试完成: {passed_tests}/{total_tests} 通过")
    
    if passed_tests == total_tests:
        print("🎉 所有认证API测试通过！")
    else:
        print("⚠️  部分测试失败，请检查API配置")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    main()
