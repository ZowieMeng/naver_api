@echo off
REM 服务状态检查脚本
REM 检查服务是否运行、端口是否开放、防火墙配置等

echo ==========================================
echo   Naver API 服务状态检查
echo ==========================================
echo.

REM 1. 检查 Python 是否安装
echo [1] 检查 Python 安装...
python --version 2>nul
if %errorLevel% equ 0 (
    echo [√] Python 已安装
) else (
    echo [×] Python 未安装或未添加到 PATH
    goto :end
)
echo.

REM 2. 检查服务是否运行
echo [2] 检查服务运行状态...
netstat -ano | findstr ":8001" >nul 2>&1
if %errorLevel% equ 0 (
    echo [√] 端口 8001 正在监听
    echo.
    echo [*] 端口详细信息:
    netstat -ano | findstr ":8001"
    echo.
) else (
    echo [×] 端口 8001 未监听 - 服务未运行
    echo [!] 请先启动服务
    goto :end
)

REM 3. 检查进程
echo [3] 检查 Python 进程...
tasklist | findstr /i "python" >nul 2>&1
if %errorLevel% equ 0 (
    echo [√] Python 进程正在运行
    echo.
    echo [*] 进程列表:
    tasklist | findstr /i "python"
    echo.
) else (
    echo [×] 未找到 Python 进程
)

REM 4. 检查防火墙规则
echo [4] 检查防火墙规则...
netsh advfirewall firewall show rule name="Naver API Service (TCP 8001)" >nul 2>&1
if %errorLevel% equ 0 (
    echo [√] 防火墙规则已配置
    echo.
    echo [*] 规则详情:
    netsh advfirewall firewall show rule name="Naver API Service (TCP 8001)"
    echo.
) else (
    echo [×] 防火墙规则未配置
    echo [!] 请运行 setup_firewall.bat 配置防火墙
    echo.
)

REM 5. 测试本地访问
echo [5] 测试本地访问...
curl -s http://localhost:8001/health >nul 2>&1
if %errorLevel% equ 0 (
    echo [√] 本地访问正常
    echo.
    echo [*] 服务响应:
    curl -s http://localhost:8001/health
    echo.
) else (
    echo [×] 本地访问失败
    echo [!] 服务可能未正常启动
    echo.
)

REM 6. 显示本机 IP 地址
echo [6] 本机 IP 地址:
echo.
ipconfig | findstr /i "IPv4"
echo.

REM 7. 测试建议
echo ==========================================
echo [*] 远程访问测试建议:
echo ==========================================
echo.
echo 从其他电脑或手机测试:
echo.

REM 获取本机 IP
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4" ^| findstr /v "127.0.0.1"') do (
    set IP=%%a
    set IP=!IP: =!
    echo   curl http://!IP!:8001/health
    echo   浏览器访问: http://!IP!:8001/docs
    echo.
)

echo ==========================================
echo [*] 故障排查步骤:
echo ==========================================
echo.
echo 如果远程无法访问:
echo   1. 确认服务已启动 (端口 8001 监听中)
echo   2. 运行 setup_firewall.bat 配置防火墙
echo   3. 检查路由器端口转发 (如需外网访问)
echo   4. 关闭 VPN 或代理
echo   5. 检查 Windows Defender 设置
echo.

:end
echo ==========================================
pause
