#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
管理员管理API测试文件
"""

import requests
import json
from datetime import datetime

# API基础URL
BASE_URL = "http://localhost:8000"

def test_admin_management():
    """测试管理员管理API"""
    print("🧪 开始测试管理员管理API...")
    print("=" * 50)
    
    # 测试数据
    test_admin = {
        "username": "test_admin",
        "password": "admin123",
        "email": "admin@test.com",
        "phone": "13800138001",
        "real_name": "测试管理员",
        "department": "信息技术部",
        "role_level": "admin",
        "permissions": ["user_manage", "system_config"]
    }
    
    admin_id = None
    
    try:
        # 1. 测试创建管理员
        print("1️⃣ 测试创建管理员...")
        response = requests.post(
            f"{BASE_URL}/admin/",
            json=test_admin,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            admin_data = response.json()
            admin_id = admin_data["id"]
            print(f"✅ 创建管理员成功，ID: {admin_id}")
            print(f"   用户名: {admin_data['username']}")
            print(f"   邮箱: {admin_data['email']}")
            print(f"   部门: {admin_data['department']}")
        else:
            print(f"❌ 创建管理员失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
            return
        
        # 2. 测试获取管理员列表
        print("\n2️⃣ 测试获取管理员列表...")
        response = requests.get(f"{BASE_URL}/admin/")
        
        if response.status_code == 200:
            admin_list = response.json()
            print(f"✅ 获取管理员列表成功")
            print(f"   总数: {admin_list['total']}")
            print(f"   当前页: {admin_list['page']}")
            print(f"   每页数量: {admin_list['page_size']}")
            print(f"   管理员数量: {len(admin_list['admins'])}")
        else:
            print(f"❌ 获取管理员列表失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
        
        # 3. 测试获取特定管理员
        print(f"\n3️⃣ 测试获取特定管理员 (ID: {admin_id})...")
        response = requests.get(f"{BASE_URL}/admin/{admin_id}")
        
        if response.status_code == 200:
            admin_info = response.json()
            print(f"✅ 获取管理员信息成功")
            print(f"   用户名: {admin_info['username']}")
            print(f"   真实姓名: {admin_info['real_name']}")
            print(f"   角色级别: {admin_info['role_level']}")
            print(f"   权限: {admin_info['permissions']}")
        else:
            print(f"❌ 获取管理员信息失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
        
        # 4. 测试更新管理员信息
        print(f"\n4️⃣ 测试更新管理员信息 (ID: {admin_id})...")
        update_data = {
            "real_name": "更新后的管理员",
            "department": "系统管理部",
            "role_level": "super_admin",
            "permissions": ["user_manage", "system_config", "admin_manage"]
        }
        
        response = requests.put(
            f"{BASE_URL}/admin/{admin_id}",
            json=update_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            updated_admin = response.json()
            print(f"✅ 更新管理员信息成功")
            print(f"   真实姓名: {updated_admin['real_name']}")
            print(f"   部门: {updated_admin['department']}")
            print(f"   角色级别: {updated_admin['role_level']}")
            print(f"   权限: {updated_admin['permissions']}")
        else:
            print(f"❌ 更新管理员信息失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
        
        # 5. 测试更新管理员密码
        print(f"\n5️⃣ 测试更新管理员密码 (ID: {admin_id})...")
        password_data = {
            "old_password": "admin123",
            "new_password": "newadmin123"
        }
        
        response = requests.put(
            f"{BASE_URL}/admin/{admin_id}/password",
            json=password_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print(f"✅ 更新管理员密码成功")
            print(f"   响应: {response.json()}")
        else:
            print(f"❌ 更新管理员密码失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
        
        # 6. 测试删除管理员（软删除）
        print(f"\n6️⃣ 测试删除管理员 (ID: {admin_id})...")
        response = requests.delete(f"{BASE_URL}/admin/{admin_id}")
        
        if response.status_code == 200:
            print(f"✅ 删除管理员成功")
            print(f"   响应: {response.json()}")
        else:
            print(f"❌ 删除管理员失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
        
        # 7. 测试恢复管理员
        print(f"\n7️⃣ 测试恢复管理员 (ID: {admin_id})...")
        response = requests.post(f"{BASE_URL}/admin/{admin_id}/restore")
        
        if response.status_code == 200:
            print(f"✅ 恢复管理员成功")
            print(f"   响应: {response.json()}")
        else:
            print(f"❌ 恢复管理员失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
        
        # 8. 测试过滤查询
        print(f"\n8️⃣ 测试过滤查询...")
        response = requests.get(f"{BASE_URL}/admin/?role_level=super_admin&is_active=true")
        
        if response.status_code == 200:
            filtered_list = response.json()
            print(f"✅ 过滤查询成功")
            print(f"   符合条件的管理员数量: {filtered_list['total']}")
        else:
            print(f"❌ 过滤查询失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
        
        print("\n" + "=" * 50)
        print("🎉 管理员管理API测试完成！")
        
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败，请确保API服务正在运行")
        print("   运行命令: python run.py")
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {str(e)}")

def test_error_cases():
    """测试错误情况"""
    print("\n🔍 测试错误情况...")
    print("=" * 30)
    
    try:
        # 测试创建重复用户名
        print("1️⃣ 测试创建重复用户名...")
        duplicate_admin = {
            "username": "test_admin",  # 重复的用户名
            "password": "admin123",
            "email": "duplicate@test.com"
        }
        
        response = requests.post(
            f"{BASE_URL}/admin/",
            json=duplicate_admin,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 400:
            print(f"✅ 正确拒绝重复用户名: {response.json()}")
        else:
            print(f"❌ 未正确处理重复用户名: {response.status_code}")
        
        # 测试获取不存在的管理员
        print("\n2️⃣ 测试获取不存在的管理员...")
        response = requests.get(f"{BASE_URL}/admin/99999")
        
        if response.status_code == 404:
            print(f"✅ 正确返回404错误: {response.json()}")
        else:
            print(f"❌ 未正确处理不存在的管理员: {response.status_code}")
        
        # 测试更新不存在的管理员
        print("\n3️⃣ 测试更新不存在的管理员...")
        update_data = {"real_name": "不存在的管理员"}
        response = requests.put(
            f"{BASE_URL}/admin/99999",
            json=update_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 404:
            print(f"✅ 正确返回404错误: {response.json()}")
        else:
            print(f"❌ 未正确处理不存在的管理员: {response.status_code}")
        
        print("\n" + "=" * 30)
        print("✅ 错误情况测试完成！")
        
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败，请确保API服务正在运行")
    except Exception as e:
        print(f"❌ 错误测试过程中发生错误: {str(e)}")

if __name__ == "__main__":
    # 运行主要测试
    test_admin_management()
    
    # 运行错误情况测试
    test_error_cases()
