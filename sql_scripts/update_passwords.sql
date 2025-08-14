-- 更新用户密码为SHA256哈希值
-- 注意：这个脚本会将明文密码更新为哈希值，与API中的验证逻辑匹配

USE user_auth_db;

-- 更新管理员密码
UPDATE users SET password = '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9' WHERE username = 'admin';

-- 更新教师密码
UPDATE users SET password = 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3' WHERE username = 'teacher_zhang';
UPDATE users SET password = '2d711642b726b04401627ca9fbac32f5c8530fb1903cc4db02258717921a4881' WHERE username = 'teacher_li';

-- 更新学生密码
UPDATE users SET password = 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3' WHERE username = 'student_wang';
UPDATE users SET password = '2d711642b726b04401627ca9fbac32f5c8530fb1903cc4db02258717921a4881' WHERE username = 'student_liu';
UPDATE users SET password = '3c9909afec25354d551dae21590bb26e38d53f2173b8d3dc3eee4c047e7ab1c1' WHERE username = 'student_chen';

-- 显示更新后的用户信息（不显示密码）
SELECT id, username, user_type, is_active, created_at FROM users ORDER BY user_type, username;
