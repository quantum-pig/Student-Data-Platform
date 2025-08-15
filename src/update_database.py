#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库更新脚本
用于更新数据库表结构，添加管理员管理所需的字段
"""

import pymysql
from config import DB_CONFIG

def update_database():
    """更新数据库表结构"""
    print("🔄 开始更新数据库表结构...")
    
    try:
        # 连接数据库
        connection = pymysql.connect(**DB_CONFIG)
        print("✅ 数据库连接成功")
        
        with connection.cursor() as cursor:
            # 检查字段是否已存在
            cursor.execute("DESCRIBE users")
            columns = [column[0] for column in cursor.fetchall()]
            
            print(f"📋 当前表字段: {columns}")
            
            # 添加缺失的字段
            if 'real_name' not in columns:
                print("➕ 添加 real_name 字段...")
                cursor.execute("ALTER TABLE users ADD COLUMN real_name VARCHAR(100) COMMENT '真实姓名' AFTER phone")
            
            if 'department' not in columns:
                print("➕ 添加 department 字段...")
                cursor.execute("ALTER TABLE users ADD COLUMN department VARCHAR(100) COMMENT '部门' AFTER real_name")
            
            if 'role_level' not in columns:
                print("➕ 添加 role_level 字段...")
                cursor.execute("ALTER TABLE users ADD COLUMN role_level ENUM('admin', 'super_admin') DEFAULT 'admin' COMMENT '角色级别' AFTER department")
            
            if 'permissions' not in columns:
                print("➕ 添加 permissions 字段...")
                cursor.execute("ALTER TABLE users ADD COLUMN permissions TEXT COMMENT '权限列表（逗号分隔）' AFTER role_level")
            
            # 更新现有管理员用户的角色级别
            print("🔄 更新现有管理员用户的角色级别...")
            cursor.execute("UPDATE users SET role_level = 'admin' WHERE user_type = 'admin'")
            
            # 为现有管理员添加默认权限
            print("🔄 为现有管理员添加默认权限...")
            cursor.execute("UPDATE users SET permissions = 'user_manage,system_config' WHERE user_type = 'admin'")
            
            # 提交更改
            connection.commit()
            print("✅ 数据库更新完成")
            
            # 显示更新后的表结构
            print("\n📋 更新后的表结构:")
            cursor.execute("DESCRIBE users")
            columns = cursor.fetchall()
            for column in columns:
                print(f"  {column[0]}: {column[1]} {column[2]} {column[3]} {column[4]} {column[5]}")
            
            # 显示管理员用户信息
            print("\n👥 管理员用户信息:")
            cursor.execute("""
                SELECT id, username, email, real_name, department, role_level, permissions, is_active 
                FROM users 
                WHERE user_type = 'admin'
            """)
            admins = cursor.fetchall()
            for admin in admins:
                print(f"  ID: {admin[0]}, 用户名: {admin[1]}, 邮箱: {admin[2]}, 真实姓名: {admin[3]}, 部门: {admin[4]}, 角色级别: {admin[5]}, 权限: {admin[6]}, 活跃: {admin[7]}")
            
    except Exception as e:
        print(f"❌ 数据库更新失败: {e}")
        if connection:
            connection.rollback()
    finally:
        if connection:
            connection.close()
            print("🔌 数据库连接已关闭")

if __name__ == "__main__":
    update_database()
