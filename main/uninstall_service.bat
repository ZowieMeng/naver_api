@echo off
chcp 65001 >nul
REM ============================================
REM 卸载 Windows 服务
REM ============================================

echo ============================================
echo 卸载 Naver Commerce Deploy API 服务
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

cd /d "%~dp0"

REM 检查 NSSM 是否存在
if not exist "nssm.exe" (
    echo [×] 错误: 未找到 nssm.exe
    pause
    exit /b 1
)

echo [*] 正在停止服务...
nssm stop NaverCommerceAPI
timeout /t 3 /nobreak >nul

echo [*] 正在卸载服务...
nssm remove NaverCommerceAPI confirm

if %errorLevel% equ 0 (
    echo [√] 服务卸载成功
) else (
    echo [!] 服务卸载可能出现问题
)

echo.
pause
