@echo off
REM Windows 防火墙规则配置脚本
REM 允许端口 8001 的入站连接
REM 需要管理员权限运行

echo ==========================================
echo   配置 Windows 防火墙规则
echo   允许远程访问 Naver API 服务
echo ==========================================
echo.

REM 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [×] 错误: 需要管理员权限运行此脚本
    echo [!] 请右键点击此文件，选择"以管理员身份运行"
    echo.
    pause
    exit /b 1
)

echo [√] 管理员权限验证通过
echo.

REM 删除已存在的规则（如果有）
echo [*] 删除旧的防火墙规则...
netsh advfirewall firewall delete rule name="Naver API Service (TCP 8001)" >nul 2>&1
netsh advfirewall firewall delete rule name="Naver API Service IN" >nul 2>&1
netsh advfirewall firewall delete rule name="Naver API Service OUT" >nul 2>&1
echo [√] 旧规则已清理
echo.

REM 获取 Python 路径
echo [*] 检测 Python 路径...
for /f "delims=" %%i in ('python -c "import sys; print(sys.executable)" 2^>nul') do set PYTHON_PATH=%%i

if not defined PYTHON_PATH (
    echo [×] 错误: 未找到 Python
    echo [!] 请确保 Python 已正确安装并添加到 PATH
    pause
    exit /b 1
)

echo [√] Python 路径: %PYTHON_PATH%
echo.

REM 添加防火墙规则 - 针对端口
echo [*] 添加防火墙规则 (端口 8001)...
netsh advfirewall firewall add rule ^
    name="Naver API Service (TCP 8001)" ^
    protocol=TCP ^
    dir=in ^
    localport=8001 ^
    action=allow ^
    description="允许访问 Naver Commerce Deploy API 服务（端口 8001）" ^
    enable=yes

if %errorLevel% equ 0 (
    echo [√] 端口 8001 入站规则添加成功
) else (
    echo [×] 端口规则添加失败
    pause
    exit /b 1
)
echo.

REM 添加防火墙规则 - 针对 Python 程序
echo [*] 添加防火墙规则 (Python 程序)...
netsh advfirewall firewall add rule ^
    name="Python for Naver API" ^
    program="%PYTHON_PATH%" ^
    protocol=TCP ^
    dir=in ^
    action=allow ^
    description="允许 Python 运行 Naver API 服务" ^
    enable=yes

if %errorLevel% equ 0 (
    echo [√] Python 程序规则添加成功
) else (
    echo [!] Python 程序规则添加失败（可能已存在）
)
echo.

REM 显示配置结果
echo ==========================================
echo [√] 防火墙配置完成！
echo ==========================================
echo.
echo [*] 已添加的规则:
netsh advfirewall firewall show rule name="Naver API Service (TCP 8001)"
echo.
echo ==========================================
echo [√] 现在可以从远程访问以下地址:
echo     http://你的服务器IP:8001
echo     http://你的服务器IP:8001/docs
echo.
echo [*] 测试步骤:
echo     1. 确保服务已启动
echo     2. 本地测试: curl http://localhost:8001/health
echo     3. 远程测试: curl http://服务器IP:8001/health
echo.
echo [*] 查看本机 IP 地址:
ipconfig | findstr /i "IPv4"
echo ==========================================
echo.
pause
