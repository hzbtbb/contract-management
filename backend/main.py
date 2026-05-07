from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.core.database import engine, Base
from app.api import auth, contracts
from app.core.config import settings

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建上传目录
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="档案管理系统", version="1.0.0")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600,
)

# 挂载静态文件目录
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(contracts.router, prefix="/api/contracts", tags=["合同"])

@app.get("/")
def root():
    return {"message": "档案管理系统API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
