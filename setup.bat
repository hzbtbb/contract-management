@echo off
chcp 65001 >nul
echo ======================================
echo 档案管理系统 - 快速启动脚本
echo ======================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到 Python
    echo 请先安装 Python 3.8 或更高版本
    pause
    exit /b 1
)

REM 检查 Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到 Node.js
    echo 请先安装 Node.js 16 或更高版本
    pause
    exit /b 1
)

echo ✓ Python 已安装
echo ✓ Node.js 已安装
echo.

REM 后端设置
echo ======================================
echo 1. 设置后端
echo ======================================
cd backend

if not exist "venv" (
    echo 创建 Python 虚拟环境...
    python -m venv venv
)

echo 激活虚拟环境...
call venv\Scripts\activate.bat

echo 安装 Python 依赖...
pip install -r requirements.txt

if not exist ".env" (
    echo 创建环境变量文件...
    copy .env.example .env
)

if not exist "contracts.db" (
    echo 初始化数据库...
    python init_db.py
)

echo.
echo ======================================
echo 2. 设置前端
echo ======================================
cd ..\frontend

if not exist "node_modules" (
    echo 安装 Node.js 依赖...
    call npm install
)

echo.
echo ======================================
echo ✓ 安装完成！
echo ======================================
echo.
echo 启动服务：
echo 1. 后端: cd backend ^&^& venv\Scripts\activate ^&^& uvicorn main:app --reload
echo 2. 前端: cd frontend ^&^& npm run dev
echo.
echo 访问地址：
echo - 前端: http://localhost:3000
echo - 后端: http://localhost:8000
echo - API 文档: http://localhost:8000/docs
echo.
echo 默认管理员账号: admin / admin123
echo ======================================
pause
