-- 更新用户密码为SHA256哈希值
-- 注意：这个脚本会将明文密码更新为哈希值，与API中的验证逻辑匹配

USE user_auth_db;

-- 更新管理员密码
UPDATE users SET password = '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9' WHERE username = 'admin';

-- 更新教师密码
UPDATE users SET password = 'cde383eee8ee7a4400adf7a15f716f179a2eb97646b37e089eb8d6d04e663416' WHERE username = 'teacher_zhang';
UPDATE users SET password = 'c4ae9d6be6070858f1555488238f26cce9c97204fb9c514bfe9ff5a6899fc524' WHERE username = 'teacher_li';

-- 更新学生密码
UPDATE users SET password = '703b0a3d6ad75b649a28adde7d83c6251da457549263bc7ff45ec709b0a8448b' WHERE username = 'student_wang';
UPDATE users SET password = '4349edb26bb041f4ec64bf736b6320e951002403c461c5df1a4705ef837b7106' WHERE username = 'student_liu';
UPDATE users SET password = '35503823ae8e063f908d703172c3fa35a7465a4c8e03f90c9c692117b3d06467' WHERE username = 'student_chen';

-- 显示更新后的用户信息（不显示密码）
SELECT id, username, user_type, is_active, created_at FROM users ORDER BY user_type, username;
