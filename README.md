# 学生数据平台 - 用户登录验证API

这是一个使用FastAPI构建的简单用户登录验证API。

## 功能特性

- 提供POST `/login` 端点用于用户登录验证
- 接受用户名和密码作为参数
- 无论输入什么参数，都返回 `True`

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行应用

```bash
python main.py
```

或者使用uvicorn直接运行：

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API文档

启动服务后，您可以访问以下地址：

- API文档：http://localhost:8000/docs
- 替代文档：http://localhost:8000/redoc

## API端点

### POST /login

用户登录验证

**请求体：**
```json
{
  "username": "用户名",
  "password": "密码"
}
```

**响应：**
```json
{
  "success": true
}
```

**示例请求：**
```bash
curl -X POST "http://localhost:8000/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "test", "password": "test123"}'
```

**示例响应：**
```json
{
  "success": true
}
```

## 项目结构

```
Student-Data-Platform/
├── main.py              # FastAPI应用主文件
├── requirements.txt     # Python依赖包
└── README.md           # 项目说明文档
```
