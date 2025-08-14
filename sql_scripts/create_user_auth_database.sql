-- 用户登录验证数据库创建脚本
-- 创建时间: 2024年
-- 描述: 用于存储用户登录验证信息的数据库

-- 创建数据库
CREATE DATABASE IF NOT EXISTS user_auth_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE user_auth_db;

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID，自增主键',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名，唯一',
    password VARCHAR(255) NOT NULL COMMENT '密码（建议使用加密存储）',
    email VARCHAR(100) COMMENT '邮箱地址，可选',
    phone VARCHAR(20) COMMENT '手机号码，可选',
    user_type ENUM('teacher', 'student', 'admin') NOT NULL DEFAULT 'student' COMMENT '用户类型：老师、学生、管理员',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    is_active BOOLEAN DEFAULT TRUE COMMENT '账户是否激活',
    last_login TIMESTAMP NULL COMMENT '最后登录时间',
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_phone (phone),
    INDEX idx_user_type (user_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户登录验证信息表';

-- 创建登录日志表（可选，用于记录登录历史）
CREATE TABLE IF NOT EXISTS login_logs (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '日志ID',
    user_id INT COMMENT '用户ID',
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '登录时间',
    login_ip VARCHAR(45) COMMENT '登录IP地址',
    user_agent TEXT COMMENT '用户代理信息',
    login_status ENUM('success', 'failed') NOT NULL COMMENT '登录状态',
    failure_reason VARCHAR(255) COMMENT '失败原因',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_login_time (login_time),
    INDEX idx_login_status (login_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户登录日志表';

-- 插入示例数据（可选）
INSERT INTO users (username, password, email, phone, user_type) VALUES
('admin', 'admin123', 'admin@example.com', '13800138000', 'admin'),
('teacher_zhang', 'teacher123', 'zhang@school.com', '13800138001', 'teacher'),
('teacher_li', 'teacher456', 'li@school.com', '13800138002', 'teacher'),
('student_wang', 'student123', 'wang@student.com', '13800138003', 'student'),
('student_liu', 'student456', 'liu@student.com', '13800138004', 'student'),
('student_chen', 'student789', 'chen@student.com', '13800138005', 'student');

-- 显示创建的表结构
DESCRIBE users;
DESCRIBE login_logs;

-- 显示数据库信息
SELECT DATABASE() as current_database;
SHOW TABLES;
