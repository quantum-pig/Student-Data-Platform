# 数据库配置文件
# 请根据实际情况修改以下配置

DB_CONFIG = {
    'host': '119.45.196.184',
    'port': 3306,
    'user': 'remote_user',  # 请修改为实际的数据库用户名
    'password': 'password',  # 请修改为实际的数据库密码
    'database': 'user_auth_db',
    'charset': 'utf8mb4',
    'autocommit': True
}

# API配置
API_CONFIG = {
    'host': '0.0.0.0',
    'port': 8000,
    'debug': True
}

# 安全配置
SECURITY_CONFIG = {
    'password_hash_algorithm': 'sha256',  # 密码哈希算法
    'session_timeout': 3600,  # 会话超时时间（秒）
}
