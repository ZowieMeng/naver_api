@echo off
chcp 65001 >nul
REM ============================================
REM Windows 服务安装脚本 (使用 NSSM)
REM ============================================

echo ============================================
echo Naver Commerce Deploy API - 服务安装
echo ============================================
echo.

REM 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [×] 错误: 需要管理员权限
    echo [!] 请右键选择"以管理员身份运行"此脚本
    pause
    exit /b 1
)

echo [√] 正在以管理员权限运行
echo.

cd /d "%~dp0"

REM 检查 Python
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [×] 错误: 未找到 Python
    pause
    exit /b 1
)
echo [√] Python 已安装
echo.

REM 检查并安装依赖包
echo [*] 检查 Python 依赖包...
python -c "import fastapi, uvicorn, pydantic, requests, bcrypt, pybase64, pytz" 2>nul
if %errorLevel% neq 0 (
    echo [!] 缺少必要的依赖包
    echo [*] 正在安装依赖包...
    pip install fastapi uvicorn pydantic requests bcrypt pybase64 pytz
    if %errorLevel% neq 0 (
        echo [×] 依赖包安装失败
        echo [!] 请手动运行: pip install fastapi uvicorn pydantic requests bcrypt pybase64 pytz
        pause
        exit /b 1
    )
    echo [√] 依赖包安装成功
) else (
    echo [√] 依赖包已安装
)
echo.

REM 检查 NSSM 是否存在
if exist "nssm.exe" (
    echo [√] NSSM 工具已存在
) else (
    echo [!] 未找到 NSSM (Non-Sucking Service Manager)
    echo [!] NSSM 是一个将程序安装为 Windows 服务的工具
    echo.
    echo [*] 请下载 NSSM:
    echo     1. 访问: https://nssm.cc/download
    echo     2. 下载最新版本 (推荐 nssm-2.24 或更高)
    echo     3. 64位系统: 解压后复制 win64\nssm.exe 到此目录
    echo        32位系统: 解压后复制 win32\nssm.exe 到此目录
    echo.
    echo [√] NSSM 完全兼容 Windows 7/8/10/11 及 Server 版本
    echo.
    echo [*] 或者使用守护进程模式 (无需 NSSM):
    echo     运行: python service_daemon.py
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================
echo 服务配置
echo ============================================
echo 服务名称: NaverCommerceAPI
echo 服务显示名: Naver Commerce Deploy API
echo 工作目录: %CD%
echo Python路径: 
python -c "import sys; print(sys.executable)"
echo ============================================
echo.

REM 停止并删除已存在的服务
nssm stop NaverCommerceAPI >nul 2>&1
nssm remove NaverCommerceAPI confirm >nul 2>&1

echo [*] 正在安装服务...

REM 获取 Python 完整路径
for /f "delims=" %%i in ('python -c "import sys; print(sys.executable)"') do set PYTHON_PATH=%%i

REM 安装服务
nssm install NaverCommerceAPI "%PYTHON_PATH%" "%CD%\deploy_api.py"

REM 设置服务参数
nssm set NaverCommerceAPI AppDirectory "%CD%"
nssm set NaverCommerceAPI DisplayName "Naver Commerce Deploy API"
nssm set NaverCommerceAPI Description "Naver 商城部署服务 - 订单查询与发货管理 API"
nssm set NaverCommerceAPI Start SERVICE_AUTO_START
nssm set NaverCommerceAPI AppStdout "%CD%\logs\service.log"
nssm set NaverCommerceAPI AppStderr "%CD%\logs\service_error.log"
nssm set NaverCommerceAPI AppRotateFiles 1
nssm set NaverCommerceAPI AppRotateSeconds 86400

REM 创建日志目录
if not exist "logs" mkdir logs

echo [√] 服务安装完成
echo.

REM 启动服务
echo [*] 正在启动服务...
nssm start NaverCommerceAPI

if %errorLevel% equ 0 (
    echo [√] 服务启动成功
    echo.
    echo ============================================
    echo [√] 服务地址: http://localhost:8001
    echo [√] API 文档: http://localhost:8001/docs
    echo [√] 日志文件: %CD%\logs\service.log
    echo ============================================
    echo.
    echo [*] 服务管理命令:
    echo     启动服务: nssm start NaverCommerceAPI
    echo     停止服务: nssm stop NaverCommerceAPI
    echo     重启服务: nssm restart NaverCommerceAPI
    echo     卸载服务: nssm remove NaverCommerceAPI confirm
    echo.
    echo [*] 或在 Windows 服务管理器中管理
    echo     运行: services.msc
    echo.
) else (
    echo [×] 服务启动失败
    echo [!] 请查看日志文件: %CD%\logs\service_error.log
)

pause
