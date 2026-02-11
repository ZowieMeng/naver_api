#!/bin/bash

# Naver Commerce Deploy API 启动脚本

echo "=================================="
echo "启动 Naver Commerce Deploy API"
echo "=================================="

# 切换到脚本所在目录
cd "$(dirname "$0")"

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3"
    exit 1
fi

# 检查依赖
echo "检查依赖包..."
python3 -c "import fastapi, uvicorn, pydantic" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  警告: 缺少必要的依赖包"
    echo "正在安装依赖..."
    pip3 install fastapi uvicorn pydantic requests bcrypt pybase64 pytz
fi

# 启动服务
echo "启动服务..."
echo "API 文档: http://localhost:8001/docs"
echo "=================================="

python3 deploy_api.py
