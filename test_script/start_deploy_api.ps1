# ============================================
# Naver Commerce Deploy API - PowerShell 启动脚本
# 支持自动重启和后台运行
# ============================================

# 设置控制台编码为 UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Naver Commerce Deploy API 启动脚本" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# 检查管理员权限
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$isAdmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if ($isAdmin) {
    Write-Host "[√] 正在以管理员权限运行" -ForegroundColor Green
} else {
    Write-Host "[!] 未以管理员权限运行" -ForegroundColor Yellow
    Write-Host "[!] 建议右键选择'以管理员身份运行'以获得更好的稳定性" -ForegroundColor Yellow
    Write-Host ""
}

# 切换到脚本所在目录
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath
Write-Host "[√] 工作目录: $scriptPath" -ForegroundColor Green
Write-Host ""

# 检查 Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[√] $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[×] 错误: 未找到 Python" -ForegroundColor Red
    Write-Host "[!] 请先安装 Python 3.8 或更高版本" -ForegroundColor Yellow
    Write-Host "[!] 下载地址: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "按 Enter 键退出"
    exit 1
}

Write-Host ""

# 检查依赖
Write-Host "[*] 检查依赖包..." -ForegroundColor Cyan
python -c "import fastapi, uvicorn, pydantic" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "[!] 缺少必要的依赖包" -ForegroundColor Yellow
    Write-Host "[*] 正在安装依赖..." -ForegroundColor Cyan
    pip install fastapi uvicorn pydantic requests bcrypt pybase64 pytz
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[×] 依赖安装失败" -ForegroundColor Red
        Read-Host "按 Enter 键退出"
        exit 1
    }
}
Write-Host "[√] 依赖包检查完成" -ForegroundColor Green
Write-Host ""

# 询问运行模式
Write-Host "请选择运行模式:" -ForegroundColor Cyan
Write-Host "  1. 前台运行 (当前窗口运行，可以看到日志)"
Write-Host "  2. 后台运行 (新窗口运行，最小化)"
Write-Host "  3. 守护模式 (自动重启，持续运行)"
Write-Host ""
$mode = Read-Host "请输入选项 (1-3)"

switch ($mode) {
    "1" {
        # 前台运行
        Write-Host ""
        Write-Host "============================================" -ForegroundColor Cyan
        Write-Host "[*] 启动服务 (前台模式)" -ForegroundColor Cyan
        Write-Host "============================================" -ForegroundColor Cyan
        Write-Host "[√] 服务地址: http://0.0.0.0:8001" -ForegroundColor Green
        Write-Host "[√] API 文档: http://localhost:8001/docs" -ForegroundColor Green
        Write-Host "============================================" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "[!] 按 Ctrl+C 可以停止服务" -ForegroundColor Yellow
        Write-Host ""
        
        python deploy_api.py
    }
    
    "2" {
        # 后台运行
        Write-Host ""
        Write-Host "[*] 正在后台启动服务..." -ForegroundColor Cyan
        
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$scriptPath'; python deploy_api.py" -WindowStyle Minimized
        
        Start-Sleep -Seconds 2
        Write-Host "[√] 服务已在后台启动" -ForegroundColor Green
        Write-Host "[√] 服务地址: http://localhost:8001" -ForegroundColor Green
        Write-Host "[√] API 文档: http://localhost:8001/docs" -ForegroundColor Green
        Write-Host ""
        Write-Host "[!] 服务正在后台运行，查看任务栏查找窗口" -ForegroundColor Yellow
        Write-Host ""
        Read-Host "按 Enter 键退出"
    }
    
    "3" {
        # 守护模式
        Write-Host ""
        Write-Host "============================================" -ForegroundColor Cyan
        Write-Host "[*] 启动服务 (守护模式)" -ForegroundColor Cyan
        Write-Host "============================================" -ForegroundColor Cyan
        Write-Host "[√] 服务地址: http://localhost:8001" -ForegroundColor Green
        Write-Host "[√] API 文档: http://localhost:8001/docs" -ForegroundColor Green
        Write-Host "[√] 自动重启: 已启用" -ForegroundColor Green
        Write-Host "============================================" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "[!] 按 Ctrl+C 可以停止服务" -ForegroundColor Yellow
        Write-Host ""
        
        # 守护进程循环
        $restartCount = 0
        while ($true) {
            if ($restartCount -gt 0) {
                Write-Host ""
                Write-Host "[!] 服务已停止，5秒后自动重启... (重启次数: $restartCount)" -ForegroundColor Yellow
                Start-Sleep -Seconds 5
                Write-Host "[*] 正在重启服务..." -ForegroundColor Cyan
            }
            
            python deploy_api.py
            $restartCount++
            
            # 如果退出码为 0，说明是正常退出，不重启
            if ($LASTEXITCODE -eq 0) {
                Write-Host "[√] 服务正常退出" -ForegroundColor Green
                break
            }
        }
    }
    
    default {
        Write-Host "[×] 无效的选项" -ForegroundColor Red
        Read-Host "按 Enter 键退出"
        exit 1
    }
}

Write-Host ""
Write-Host "[!] 服务已停止" -ForegroundColor Yellow
Read-Host "按 Enter 键退出"
