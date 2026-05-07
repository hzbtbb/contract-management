# 档案管理系统

一个基于 Vue 3 + FastAPI 的合同档案管理系统，支持合同上传、查看、下载、统计分析等功能。

## 技术栈

### 前端
- **Vue 3.3.4** - 渐进式 JavaScript 框架
- **Vite 4.4.9** - 前端构建工具
- **Element Plus 2.3.14** - UI 组件库
- **Vue Router 4.2.4** - 路由管理
- **Pinia 2.1.6** - 状态管理
- **Axios 1.5.0** - HTTP 客户端
- **ECharts 5.4.3** - 数据可视化

### 后端
- **Python 3.11+**
- **FastAPI 0.109.0** - 现代 Web 框架
- **Uvicorn 0.27.0** - ASGI 服务器
- **SQLAlchemy 2.0.25** - ORM 框架
- **Pydantic 2.5.3** - 数据验证
- **Python-Jose 3.3.0** - JWT 认证
- **Passlib 1.7.4** + **Bcrypt 4.0.1** - 密码加密

### 数据库
- **SQLite 3** - 轻量级关系型数据库（开发环境）
- 支持迁移至 **PostgreSQL** 或 **MySQL**（生产环境）

## 功能特性

### 用户管理
- 用户登录/登出
- 角色权限控制（管理员/普通用户）
- 用户增删改查（仅管理员）
- 科室管理

### 合同管理
- 合同上传（支持 PDF、图片格式）
- 合同列表查看（支持科室筛选）
- 合同详情查看
- 合同编辑/删除
- 合同下载（自动统计下载次数）
- 科室权限隔离（普通用户只能查看本科室合同）

### 数据统计
- 仪表板数据可视化
- 合同数量统计
- 合同金额统计
- 按科室分类统计
- 按年份筛选统计

## 环境要求

- **Node.js**: 18.x 或更高版本
- **Python**: 3.11 或更高版本
- **npm**: 9.x 或更高版本

## 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd 档案管理系统
```

### 2. 后端配置

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python -c "
from app.core.database import engine, Base
from app.models.models import User, Contract
from app.crud.user import create_user
from app.core.database import SessionLocal

Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    admin = create_user(db, 'admin', 'admin123', None, 'admin')
    print('数据库初始化成功')
finally:
    db.close()
"

# 启动后端服务
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

后端服务将运行在 `http://localhost:8000`

### 3. 前端配置

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务将运行在 `http://localhost:5173`

### 4. 默认账号

- **管理员账号**: admin / admin123
- 首次登录后建议修改密码

## 项目结构

```
档案管理系统/
├── backend/                 # 后端项目
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── core/           # 核心配置
│   │   ├── crud/           # 数据库操作
│   │   ├── models/         # 数据模型
│   │   └── schemas/        # Pydantic 模型
│   ├── uploads/            # 文件上传目录
│   ├── main.py             # 应用入口
│   └── requirements.txt    # Python 依赖
│
└── frontend/               # 前端项目
    ├── src/
    │   ├── api/           # API 接口
    │   ├── components/    # 公共组件
    │   ├── router/        # 路由配置
    │   ├── store/         # 状态管理
    │   ├── utils/         # 工具函数
    │   └── views/         # 页面组件
    ├── package.json       # Node 依赖
    └── vite.config.js     # Vite 配置
```

## 生产环境部署

### 后端部署

#### 1. 使用 Gunicorn + Uvicorn

```bash
# 安装 Gunicorn
pip install gunicorn

# 启动服务（4 个工作进程）
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

#### 2. 使用 Systemd 服务

创建 `/etc/systemd/system/contract-api.service`:

```ini
[Unit]
Description=Contract Management API
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/path/to/backend
Environment="PATH=/path/to/backend/venv/bin"
ExecStart=/path/to/backend/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable contract-api
sudo systemctl start contract-api
```

#### 3. 数据库迁移（生产环境推荐 PostgreSQL）

修改 `backend/app/core/config.py`:

```python
DATABASE_URL = "postgresql://user:password@localhost/dbname"
```

安装 PostgreSQL 驱动：

```bash
pip install psycopg2-binary
```

### 前端部署

#### 1. 构建生产版本

```bash
cd frontend
npm run build
```

构建产物在 `dist/` 目录

#### 2. 使用 Nginx 部署

创建 Nginx 配置 `/etc/nginx/sites-available/contract-management`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API 代理
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 文件上传大小限制
    client_max_body_size 50M;
}
```

启用配置：

```bash
sudo ln -s /etc/nginx/sites-available/contract-management /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 3. 使用 Docker 部署

创建 `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend/uploads:/app/uploads
      - ./backend/contracts.db:/app/contracts.db
    environment:
      - DATABASE_URL=sqlite:///./contracts.db
    restart: always

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: always
```

后端 `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]
```

前端 `Dockerfile`:

```dockerfile
FROM node:18-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

启动：

```bash
docker-compose up -d
```

## 配置说明

### 后端配置

编辑 `backend/app/core/config.py`:

```python
class Settings(BaseSettings):
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./contracts.db"
    
    # JWT 配置
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24小时
    
    # 文件上传配置
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50MB
```

### 前端配置

编辑 `frontend/src/utils/request.js`:

```javascript
const baseURL = import.meta.env.VITE_API_BASE_URL || '/api'
```

创建 `.env.production`:

```
VITE_API_BASE_URL=https://your-domain.com/api
```

## 常见问题

### 1. 端口被占用

```bash
# 查看端口占用
lsof -i :8000
lsof -i :5173

# 杀死进程
kill -9 <PID>
```

### 2. 数据库迁移

```bash
# 备份数据库
cp contracts.db contracts.db.backup

# 重新初始化
rm contracts.db
python init_db.py
```

### 3. 文件上传失败

检查 `uploads/` 目录权限：

```bash
chmod 755 uploads/
```

### 4. CORS 错误

确保后端 `main.py` 中配置了正确的 CORS：

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 开发环境
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 安全建议

1. **修改默认密钥**: 生产环境必须修改 `SECRET_KEY`
2. **使用 HTTPS**: 生产环境启用 SSL/TLS
3. **定期备份**: 定期备份数据库和上传文件
4. **限制文件类型**: 只允许必要的文件格式上传
5. **日志监控**: 启用访问日志和错误日志
6. **防火墙配置**: 只开放必要的端口

## 维护与监控

### 日志查看

```bash
# 后端日志
tail -f backend.log

# Nginx 日志
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Systemd 服务日志
journalctl -u contract-api -f
```

### 数据库备份

```bash
# SQLite 备份
sqlite3 contracts.db ".backup contracts_backup.db"

# PostgreSQL 备份
pg_dump dbname > backup.sql
```

## 许可证

MIT License

## 联系方式

如有问题或建议，请联系项目维护者。
