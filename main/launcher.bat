@echo off
chcp 65001 >nul
title Naver Commerce Deploy API - 启动选择器

:MENU
cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║       Naver Commerce Deploy API - 启动选择器              ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo  请选择运行方式:
echo.
echo  [1] 前台运行 (简单模式)
echo      - 在当前窗口运行
echo      - 可以看到实时日志
echo      - 适合测试和开发
echo.
echo  [2] 后台运行 (新窗口)
echo      - 在新窗口运行
echo      - 最小化到后台
echo      - 方便多任务
echo.
echo  [3] 守护进程 (自动重启)
echo      - 自动监控和重启
echo      - 服务崩溃自动恢复
echo      - 适合长期运行
echo.
echo  [4] 安装 Windows 服务 (推荐生产环境)
echo      - 开机自动启动
echo      - 完全后台运行
echo      - 系统级服务管理
echo      - 需要管理员权限
echo      - 兼容 Windows 7/8/10/11
echo.
echo  [5] 卸载 Windows 服务
echo      - 移除已安装的服务
echo      - 需要管理员权限
echo.
echo  [6] 查看服务状态
echo      - 检查服务是否运行
echo      - 查看端口占用
echo.
echo  [0] 退出
echo.
echo ════════════════════════════════════════════════════════════
echo.
set /p choice="请输入选项 (0-6): "

if "%choice%"=="1" goto FOREGROUND
if "%choice%"=="2" goto BACKGROUND
if "%choice%"=="3" goto DAEMON
if "%choice%"=="4" goto INSTALL_SERVICE
if "%choice%"=="5" goto UNINSTALL_SERVICE
if "%choice%"=="6" goto CHECK_STATUS
if "%choice%"=="0" goto EXIT
echo.
echo [×] 无效的选项，请重新选择
timeout /t 2 >nul
goto MENU

:FOREGROUND
cls
echo.
echo ════════════════════════════════════════════════════════════
echo  启动模式: 前台运行
echo ════════════════════════════════════════════════════════════
echo.
call start_deploy_api.bat
goto MENU

:BACKGROUND
cls
echo.
echo ════════════════════════════════════════════════════════════
echo  启动模式: 后台运行
echo ════════════════════════════════════════════════════════════
echo.
echo [*] 正在启动服务（新窗口）...
start "Naver API Service" /MIN cmd /k "cd /d "%~dp0" && start_deploy_api.bat"
timeout /t 2 >nul
echo [√] 服务已在后台启动
echo [√] 查看任务栏找到窗口
echo [√] 服务地址: http://localhost:8001
echo.
pause
goto MENU

:DAEMON
cls
echo.
echo ════════════════════════════════════════════════════════════
echo  启动模式: 守护进程（自动重启）
echo ════════════════════════════════════════════════════════════
echo.
python service_daemon.py
pause
goto MENU

:INSTALL_SERVICE
cls
echo.
echo ════════════════════════════════════════════════════════════
echo  安装 Windows 服务
echo ════════════════════════════════════════════════════════════
echo.
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [×] 错误: 需要管理员权限
    echo [!] 请右键选择"以管理员身份运行"此脚本
    echo.
    pause
    goto MENU
)
echo [√] 正在以管理员权限运行
echo.
call install_service.bat
goto MENU

:UNINSTALL_SERVICE
cls
echo.
echo ════════════════════════════════════════════════════════════
echo  卸载 Windows 服务
echo ════════════════════════════════════════════════════════════
echo.
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [×] 错误: 需要管理员权限
    echo [!] 请右键选择"以管理员身份运行"此脚本
    echo.
    pause
    goto MENU
)
echo [√] 正在以管理员权限运行
echo.
call uninstall_service.bat
goto MENU

:CHECK_STATUS
cls
echo.
echo ════════════════════════════════════════════════════════════
echo  服务状态检查
echo ════════════════════════════════════════════════════════════
echo.

REM 检查 Windows 服务状态
if exist "nssm.exe" (
    echo [*] Windows 服务状态:
    nssm status NaverCommerceAPI 2>nul
    if %errorLevel% equ 0 (
        echo [√] 服务正在运行
    ) else (
        echo [!] 服务未运行或未安装
    )
    echo.
)

REM 检查端口占用
echo [*] 端口 8001 状态:
netstat -ano | findstr :8001 >nul
if %errorLevel% equ 0 (
    echo [√] 端口 8001 正在使用
    netstat -ano | findstr :8001
) else (
    echo [!] 端口 8001 未被占用
)
echo.

REM 检查 Python 进程
echo [*] Python 进程:
tasklist | findstr python.exe >nul
if %errorLevel% equ 0 (
    echo [√] 发现 Python 进程:
    tasklist | findstr python.exe
) else (
    echo [!] 未发现 Python 进程
)
echo.

REM 测试服务连接
echo [*] 尝试连接服务...
curl -s http://localhost:8001/health >nul 2>&1
if %errorLevel% equ 0 (
    echo [√] 服务响应正常
    echo [√] 服务地址: http://localhost:8001
    echo [√] API 文档: http://localhost:8001/docs
) else (
    echo [!] 服务未响应
)
echo.
echo ════════════════════════════════════════════════════════════
echo.
pause
goto MENU

:EXIT
cls
echo.
echo ════════════════════════════════════════════════════════════
echo  感谢使用 Naver Commerce Deploy API
echo ════════════════════════════════════════════════════════════
echo.
echo  API 文档: http://localhost:8001/docs
echo  帮助文档: WINDOWS_DEPLOY.md
echo.
exit /b 0
