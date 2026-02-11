@echo off
chcp 65001 >nul
REM ============================================
REM Naver Commerce Deploy API - Windows 启动脚本
REM ============================================

echo ============================================
echo Naver Commerce Deploy API 启动脚本
echo ============================================
echo.

REM 检查管理员权限
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [√] 正在以管理员权限运行
) else (
    echo [!] 未以管理员权限运行
    echo [!] 建议右键选择"以管理员身份运行"以获得更好的稳定性
    echo.
)

REM 切换到脚本所在目录
cd /d "%~dp0"
echo [√] 工作目录: %CD%
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [×] 错误: 未找到 Python
    echo [!] 请先安装 Python 3.8 或更高版本
    echo [!] 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [√] Python 版本:
python --version
echo.

REM 检查依赖包
echo [*] 检查依赖包...
python -c "import fastapi, uvicorn, pydantic" 2>nul
if %errorLevel% neq 0 (
    echo [!] 缺少必要的依赖包
    echo [*] 正在安装依赖...
    pip install fastapi uvicorn pydantic requests bcrypt pybase64 pytz
    if %errorLevel% neq 0 (
        echo [×] 依赖安装失败
        pause
        exit /b 1
    )
)
echo [√] 依赖包检查完成
echo.

REM 启动服务
echo ============================================
echo [*] 启动 Naver Commerce Deploy API 服务
echo ============================================
echo [√] 服务地址: http://0.0.0.0:8001
echo [√] API 文档: http://localhost:8001/docs
echo ============================================
echo.
echo [!] 按 Ctrl+C 可以停止服务
echo.

REM 启动 Python 服务
python deploy_api.py

REM 如果服务意外退出
echo.
echo [!] 服务已停止
pause
