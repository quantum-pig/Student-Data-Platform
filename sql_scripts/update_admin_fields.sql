-- 管理员管理字段更新脚本
-- 为users表添加管理员管理所需的字段

USE user_auth_db;

-- 添加管理员管理相关字段
ALTER TABLE users 
ADD COLUMN real_name VARCHAR(100) COMMENT '真实姓名' AFTER phone,
ADD COLUMN department VARCHAR(100) COMMENT '部门' AFTER real_name,
ADD COLUMN role_level ENUM('admin', 'super_admin') DEFAULT 'admin' COMMENT '角色级别' AFTER department,
ADD COLUMN permissions TEXT COMMENT '权限列表（逗号分隔）' AFTER role_level;

-- 更新现有管理员用户的角色级别
UPDATE users SET role_level = 'admin' WHERE user_type = 'admin';

-- 为现有管理员添加默认权限
UPDATE users SET permissions = 'user_manage,system_config' WHERE user_type = 'admin';

-- 显示更新后的表结构
DESCRIBE users;

-- 显示管理员用户信息
SELECT id, username, email, real_name, department, role_level, permissions, is_active 
FROM users 
WHERE user_type = 'admin';
