#!/bin/bash

echo "======================================"
echo "档案管理系统 - 快速启动脚本"
echo "======================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 3"
    echo "请先安装 Python 3.8 或更高版本"
    exit 1
fi

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 错误: 未找到 Node.js"
    echo "请先安装 Node.js 16 或更高版本"
    exit 1
fi

echo "✓ Python 版本: $(python3 --version)"
echo "✓ Node.js 版本: $(node --version)"
echo ""

# 后端设置
echo "======================================"
echo "1. 设置后端"
echo "======================================"
cd backend

if [ ! -d "venv" ]; then
    echo "创建 Python 虚拟环境..."
    python3 -m venv venv
fi

echo "激活虚拟环境..."
source venv/bin/activate

echo "安装 Python 依赖..."
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    echo "创建环境变量文件..."
    cp .env.example .env
fi

if [ ! -f "contracts.db" ]; then
    echo "初始化数据库..."
    python init_db.py
fi

echo ""
echo "======================================"
echo "2. 设置前端"
echo "======================================"
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "安装 Node.js 依赖..."
    npm install
fi

echo ""
echo "======================================"
echo "✓ 安装完成！"
echo "======================================"
echo ""
echo "启动服务："
echo "1. 后端: cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "2. 前端: cd frontend && npm run dev"
echo ""
echo "访问地址："
echo "- 前端: http://localhost:3000"
echo "- 后端: http://localhost:8000"
echo "- API 文档: http://localhost:8000/docs"
echo ""
echo "默认管理员账号: admin / admin123"
echo "======================================"
