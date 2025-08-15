#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户管理API测试脚本
用于测试用户管理的增删改查功能
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

def test_create_user():
    """测试创建用户"""
    print("=== 测试创建用户 ===")
    
    # 测试数据
    test_users = [
        {
            "username": "test_student",
            "password": "test123",
            "email": "test_student@example.com",
            "phone": "13800138010",
            "user_type": "student"
        },
        {
            "username": "test_teacher",
            "password": "test456",
            "email": "test_teacher@example.com",
            "phone": "13800138011",
            "user_type": "teacher"
        }
    ]
    
    created_users = []
    
    for i, user_data in enumerate(test_users):
        try:
            response = requests.post(f"{BASE_URL}/users/", json=user_data)
            print(f"创建用户 {i+1}: {user_data['username']}")
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 创建成功: {result['username']} (ID: {result['id']})")
                created_users.append(result)
            else:
                print(f"❌ 创建失败: {response.text}")
                
        except Exception as e:
            print(f"❌ 请求异常: {e}")
        
        print("-" * 50)
    
    return created_users

def test_get_users():
    """测试获取用户列表"""
    print("=== 测试获取用户列表 ===")
    
    # 测试不同的查询参数
    test_cases = [
        {"page": 1, "page_size": 5},
        {"page": 1, "page_size": 10, "user_type": "student"},
        {"page": 1, "page_size": 10, "is_active": True},
        {"page": 1, "page_size": 10, "search": "test"}
    ]
    
    for i, params in enumerate(test_cases):
        try:
            response = requests.get(f"{BASE_URL}/users/", params=params)
            print(f"查询 {i+1}: {params}")
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 查询成功: 总数 {result['total']}, 当前页 {len(result['users'])} 个用户")
                for user in result['users'][:3]:  # 只显示前3个用户
                    print(f"  - {user['username']} ({user['user_type']})")
            else:
                print(f"❌ 查询失败: {response.text}")
                
        except Exception as e:
            print(f"❌ 请求异常: {e}")
        
        print("-" * 50)

def test_get_single_user(user_id: int):
    """测试获取单个用户"""
    print(f"=== 测试获取单个用户 (ID: {user_id}) ===")
    
    try:
        response = requests.get(f"{BASE_URL}/users/{user_id}")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 获取成功: {result['username']} ({result['user_type']})")
            print(f"  邮箱: {result['email']}")
            print(f"  手机: {result['phone']}")
            print(f"  状态: {'激活' if result['is_active'] else '禁用'}")
        else:
            print(f"❌ 获取失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
    
    print("-" * 50)

def test_update_user(user_id: int):
    """测试更新用户"""
    print(f"=== 测试更新用户 (ID: {user_id}) ===")
    
    # 更新数据
    update_data = {
        "email": "updated_email@example.com",
        "phone": "13800138099",
        "user_type": "teacher"
    }
    
    try:
        response = requests.put(f"{BASE_URL}/users/{user_id}", json=update_data)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 更新成功: {result['username']}")
            print(f"  新邮箱: {result['email']}")
            print(f"  新手机: {result['phone']}")
            print(f"  新类型: {result['user_type']}")
        else:
            print(f"❌ 更新失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
    
    print("-" * 50)

def test_reset_password(user_id: int):
    """测试重置密码"""
    print(f"=== 测试重置密码 (ID: {user_id}) ===")
    
    new_password = "newpassword123"
    
    try:
        response = requests.post(f"{BASE_URL}/users/{user_id}/reset-password", 
                               params={"new_password": new_password})
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 密码重置成功: {result['message']}")
        else:
            print(f"❌ 密码重置失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
    
    print("-" * 50)

def test_delete_user(user_id: int):
    """测试删除用户"""
    print(f"=== 测试删除用户 (ID: {user_id}) ===")
    
    try:
        response = requests.delete(f"{BASE_URL}/users/{user_id}")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 删除成功: {result['message']}")
        else:
            print(f"❌ 删除失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
    
    print("-" * 50)

def main():
    """主测试函数"""
    print("开始用户管理API测试...")
    print("=" * 60)
    
    # 1. 测试创建用户
    created_users = test_create_user()
    
    if not created_users:
        print("❌ 没有成功创建用户，跳过后续测试")
        return
    
    # 2. 测试获取用户列表
    test_get_users()
    
    # 3. 测试获取单个用户
    test_user = created_users[0]
    test_get_single_user(test_user['id'])
    
    # 4. 测试更新用户
    test_update_user(test_user['id'])
    
    # 5. 测试重置密码
    test_reset_password(test_user['id'])
    
    # 6. 测试删除用户
    test_delete_user(test_user['id'])
    
    print("=" * 60)
    print("用户管理API测试完成！")
    print("💡 提示：删除的用户可以通过更新 is_active 字段重新激活")

if __name__ == "__main__":
    main()
