@echo off
REM 代码更新和服务重启脚本 (Windows)
REM 用法: update_deploy.bat [选项]

setlocal enabledelayedexpansion

REM 配置
set "API_URL=http://localhost:8001"
set "SECRET_KEY=naver_deploy_2026"

REM 从环境变量读取（如果存在）
if defined DEPLOY_SECRET_KEY set "SECRET_KEY=%DEPLOY_SECRET_KEY%"

REM 默认参数
set "INSTALL_DEPS=true"
set "RESTART_SERVICE=true"
set "CHECK_ONLY=false"

REM 解析命令行参数
:parse_args
if "%~1"=="" goto :check_action
if /i "%~1"=="--help" goto :show_help
if /i "%~1"=="-h" goto :show_help
if /i "%~1"=="--no-deps" (
    set "INSTALL_DEPS=false"
    shift
    goto :parse_args
)
if /i "%~1"=="--no-restart" (
    set "RESTART_SERVICE=false"
    shift
    goto :parse_args
)
if /i "%~1"=="--check" (
    set "CHECK_ONLY=true"
    shift
    goto :parse_args
)
if /i "%~1"=="--url" (
    set "API_URL=%~2"
    shift
    shift
    goto :parse_args
)
if /i "%~1"=="--key" (
    set "SECRET_KEY=%~2"
    shift
    shift
    goto :parse_args
)
echo [×] 未知选项: %~1
echo 使用 --help 查看帮助信息
goto :error

:show_help
echo ==================================
echo   代码更新和服务重启脚本
echo ==================================
echo.
echo 用法: %~nx0 [选项]
echo.
echo 选项:
echo   -h, --help              显示此帮助信息
echo   --no-deps               不安装依赖包
echo   --no-restart            不重启服务
echo   --check                 只检查服务状态
echo   --url URL               指定 API 地址 (默认: http://localhost:8001)
echo   --key KEY               指定密钥 (默认: naver_deploy_2026)
echo.
echo 示例:
echo   %~nx0                      # 完整更新（拉取代码 + 安装依赖 + 重启）
echo   %~nx0 --no-deps            # 只拉取代码和重启，不安装依赖
echo   %~nx0 --no-restart         # 只拉取代码和安装依赖，不重启
echo   %~nx0 --check              # 检查服务状态
echo.
echo 环境变量:
echo   DEPLOY_SECRET_KEY       部署密钥
echo.
goto :end

:check_action
if "%CHECK_ONLY%"=="true" goto :check_service
goto :update_deploy

:check_service
echo ==================================
echo [*] 检查服务状态...
echo ==================================

curl -s "%API_URL%/health" > %TEMP%\health_response.json 2>nul

if %errorlevel% equ 0 (
    echo [√] 服务运行正常
    type %TEMP%\health_response.json
    del %TEMP%\health_response.json 2>nul
    goto :success
) else (
    echo [×] 服务未运行或状态异常
    del %TEMP%\health_response.json 2>nul
    goto :error
)

:update_deploy
echo ==================================
echo [*] 开始更新部署
echo ==================================
echo [*] API 地址: %API_URL%
echo [*] 安装依赖: %INSTALL_DEPS%
echo [*] 重启服务: %RESTART_SERVICE%
echo ==================================
echo.

REM 创建临时 JSON 文件
set "JSON_FILE=%TEMP%\deploy_update.json"
(
    echo {
    echo   "secret_key": "%SECRET_KEY%",
    echo   "install_dependencies": %INSTALL_DEPS%,
    echo   "restart_service": %RESTART_SERVICE%
    echo }
) > "%JSON_FILE%"

echo [*] 发送更新请求...

REM 发送请求
curl -s -X POST "%API_URL%/api/deploy/update" ^
    -H "Content-Type: application/json" ^
    -d @"%JSON_FILE%" ^
    -w "%%{http_code}" ^
    -o %TEMP%\deploy_response.json

set "HTTP_CODE=%errorlevel%"

echo ==================================
echo [*] 处理响应...
echo ==================================

REM 读取响应
if exist %TEMP%\deploy_response.json (
    type %TEMP%\deploy_response.json
    
    REM 检查响应中是否包含 "success": true
    findstr /C:"\"success\": true" %TEMP%\deploy_response.json >nul
    if %errorlevel% equ 0 (
        echo.
        echo ==================================
        echo [√] 更新成功!
        echo ==================================
        
        if "%RESTART_SERVICE%"=="true" (
            echo.
            echo [*] 服务将在 2 秒后重启，等待 5 秒后检查状态...
            timeout /t 5 /nobreak >nul
            echo.
            call :check_service
        )
        
        del "%JSON_FILE%" 2>nul
        del %TEMP%\deploy_response.json 2>nul
        goto :success
    ) else (
        echo.
        echo ==================================
        echo [×] 更新失败
        echo ==================================
        del "%JSON_FILE%" 2>nul
        del %TEMP%\deploy_response.json 2>nul
        goto :error
    )
) else (
    echo [×] 无法连接到服务
    del "%JSON_FILE%" 2>nul
    goto :error
)

:success
endlocal
exit /b 0

:error
endlocal
exit /b 1

:end
endlocal
exit /b 0
