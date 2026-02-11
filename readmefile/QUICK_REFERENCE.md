# 快速参考 - Windows 部署

## ✅ Windows 11 完全兼容

所有部署方式都已在 **Windows 11** 上测试通过：
- ✅ BAT 批处理脚本
- ✅ PowerShell 脚本  
- ✅ Python 守护进程
- ✅ NSSM Windows 服务（完全兼容 Win11）

## 📌 最快部署方式

### 测试/开发环境
```bash
双击运行: start_deploy_api.bat
```

### 生产环境（推荐）
```bash
1. 下载 NSSM: https://nssm.cc/download
2. 64位系统使用 win64\nssm.exe（推荐）
3. 复制 nssm.exe 到此目录
4. 右键"以管理员身份运行": install_service.bat
```

**NSSM 兼容性：** ✅ 完全支持 Windows 11/10/8/7

## 🎯 四种运行方式对比

| 方式 | 命令 | 开机自启 | 自动重启 | 后台运行 |
|------|------|---------|---------|---------|
| 1️⃣ BAT 脚本 | `start_deploy_api.bat` | ❌ | ❌ | ❌ |
| 2️⃣ PowerShell | `start_deploy_api.ps1` | ❌ | ✅ | ✅ |
| 3️⃣ Python 守护 | `python service_daemon.py` | ❌ | ✅ | ❌ |
| 4️⃣ Windows 服务 | `install_service.bat` | ✅ | ✅ | ✅ |

## ⚡ 常用命令

### 服务启动
```bash
# 方式 1: 批处理（最简单）
start_deploy_api.bat

# 方式 2: PowerShell（功能丰富）
powershell -ExecutionPolicy Bypass -File start_deploy_api.ps1

# 方式 3: Python 守护进程
python service_daemon.py

# 方式 4: Windows 服务
nssm start NaverCommerceAPI
```

### 服务管理
```bash
# 停止服务
nssm stop NaverCommerceAPI

# 重启服务
nssm restart NaverCommerceAPI

# 查看服务状态
nssm status NaverCommerceAPI

# 卸载服务
uninstall_service.bat
```

### 进程管理
```bash
# 查看 Python 进程
tasklist | findstr python

# 结束进程（PID 从上面查到）
taskkill /PID <PID> /F

# 强制结束所有 Python 进程
taskkill /IM python.exe /F
```

### 端口检查
```bash
# 查看端口占用
netstat -ano | findstr :8001

# 查看哪个程序占用端口
for /f "tokens=5" %a in ('netstat -ano ^| findstr :8001') do @echo %a & tasklist | findstr %a
```

## 🔧 快速故障排除

### 问题：端口被占用
```bash
# 1. 查找占用进程
netstat -ano | findstr :8001

# 2. 结束进程
taskkill /PID <进程ID> /F

# 3. 或修改端口（编辑 deploy_api.py，port=8002）
```

### 问题：PowerShell 脚本无法运行
```powershell
# 以管理员身份运行 PowerShell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 问题：缺少依赖
```bash
# 安装所有依赖
pip install fastapi uvicorn pydantic requests bcrypt pybase64 pytz
```

### 问题：服务无法启动
```bash
# 1. 检查日志
type logs\service_error.log

# 2. 手动测试
python deploy_api.py

# 3. 查看详细错误
```

## 🌐 访问地址

- **服务地址**: http://localhost:8001
- **API 文档**: http://localhost:8001/docs
- **健康检查**: http://localhost:8001/health

## 🔍 测试命令

```bash
# 健康检查
curl http://localhost:8001/health

# 或在浏览器中打开
start http://localhost:8001/docs
```

## 📁 重要文件位置

```
deploy_code/
├── deploy_api.py              ← 主服务文件
├── start_deploy_api.bat       ← 批处理启动脚本
├── start_deploy_api.ps1       ← PowerShell 启动脚本
├── service_daemon.py          ← Python 守护进程
├── install_service.bat        ← 服务安装脚本
└── logs/                      ← 日志目录（服务模式）
    ├── service.log            ← 标准日志
    └── service_error.log      ← 错误日志
```

## 🔐 管理员权限

某些操作需要管理员权限：

1. **右键文件** → "以管理员身份运行"
2. 或在管理员 PowerShell 中运行：
   ```powershell
   Start-Process powershell -Verb runAs
   ```
NSSM 详细指南**: [NSSM_GUIDE.md](NSSM_GUIDE.md) ⭐ Windows 11 兼容性说明
- **
## 📚 详细文档

- **完整部署指南**: [WINDOWS_DEPLOY.md](WINDOWS_DEPLOY.md)
- **基础文档**: [README.md](README.md)
- **参数说明**: [PARAMS_GUIDE.md](PARAMS_GUIDE.md)
- **更新日志**: [CHANGELOG.md](CHANGELOG.md)

## 💡 最佳实践

### 开发环境
```bash
# 使用 PowerShell 守护模式
start_deploy_api.ps1
→ 选择模式 3（守护模式）
```

### 生产环境
```bash
# 安装为 Windows 服务
install_service.bat
# 优势：开机自启、自动重启、后台运行
```

## 🚨 紧急情况

### 立即停止所有服务
```bash
# 停止 Windows 服务
nssm stop NaverCommerceAPI

# 强制结束所有 Python 进程
taskkill /IM python.exe /F
```

### 完全重置
```bash
# 1. 卸载服务
uninstall_service.bat

# 2. 清理进程
taskkill /IM python.exe /F

# 3. 重新安装
install_service.bat
```

---

**需要帮助？** 查看 [WINDOWS_DEPLOY.md](WINDOWS_DEPLOY.md) 获取详细说明。
