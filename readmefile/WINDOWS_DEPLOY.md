# Windows 部署指南

本文档介绍如何在 Windows 系统上部署和运行 Naver Commerce Deploy API 服务。

## 🚀 快速开始

### 方式 1: 批处理脚本（最简单）

双击运行 `start_deploy_api.bat`

或右键选择"以管理员身份运行"以获得更好的稳定性。

### 方式 2: PowerShell 脚本（推荐）

右键选择 `start_deploy_api.ps1` → "使用 PowerShell 运行"

或右键选择"以管理员身份运行"。

**提供三种运行模式:**
- **前台运行** - 在当前窗口运行，可以看到实时日志
- **后台运行** - 在新窗口运行并最小化
- **守护模式** - 自动重启，服务崩溃后自动恢复

### 方式 3: Python 守护进程（自动重启）

```bash
python service_daemon.py
```

此方式提供：
- ✅ 自动重启功能
- ✅ 日志输出
- ✅ 防止频繁重启保护
- ✅ 优雅退出支持

### 方式 4: Windows 服务（持久运行）

**需要管理员权限**

#### NSSM 简介

NSSM (Non-Sucking Service Manager) 是一个开源的 Windows 服务管理工具，可以将任何程序安装为 Windows 服务。

**兼容性：**
- ✅ **Windows 11** (完全兼容，已测试)
- ✅ Windows 10
- ✅ Windows 8/8.1
- ✅ Windows 7
- ✅ Windows Server 2008 R2 及更高版本

**最新版本：** NSSM 2.24（2014年发布，依然完美兼容最新的 Windows 11）

#### 安装步骤

1. **下载 NSSM**
   - 官方网站: https://nssm.cc/download
   - 推荐下载: nssm-2.24.zip 或更高版本
   - 解压后根据系统选择：
     - **64位系统（推荐）**：使用 `win64/nssm.exe`
     - 32位系统：使用 `win32/nssm.exe`
   - 将 `nssm.exe` 复制到 `deploy_code` 目录

2. 右键"以管理员身份运行" `install_service.bat`

3. 服务将自动安装并启动

> 📖 **NSSM 详细使用指南：** [NSSM_GUIDE.md](NSSM_GUIDE.md)

**服务管理命令:**
```bash
# 启动服务
nssm start NaverCommerceAPI

# 停止服务
nssm stop NaverCommerceAPI

# 重启服务
nssm restart NaverCommerceAPI

# 卸载服务
nssm remove NaverCommerceAPI confirm
```

或在 Windows 服务管理器中管理（运行 `services.msc`）。

## 📋 系统要求

- **Windows 7/8/10/11** 或 Windows Server 2008 R2 及更高版本
- **Python 3.8** 或更高版本
- **管理员权限**（推荐，某些功能必需）

### ✅ Windows 11 兼容性

本服务已在 Windows 11 上测试通过，所有功能完全兼容：
- ✅ NSSM 服务安装（完全兼容 Windows 11）
- ✅ PowerShell 脚本
- ✅ 批处理脚本
- ✅ Python 守护进程

**Windows 11 额外注意事项：**
- Windows 11 的安全设置更严格，请确保以管理员身份运行
- 如果遇到 SmartScreen 警告，选择"仍要运行"
- 建议使用 Windows Terminal 获得更好的体验

> 📖 **详细说明：** [WINDOWS11_NOTES.md](WINDOWS11_NOTES.md) - Windows 11 特定注意事项和优化建议

## 🔧 安装依赖

自动安装（推荐）：
```bash
# 运行启动脚本会自动检查并安装依赖
start_deploy_api.bat
```

手动安装：
```bash
pip install -r ../requirements.txt
```

或：
```bash
pip install fastapi uvicorn pydantic requests bcrypt pybase64 pytz
```

## 📁 文件说明

| 文件 | 说明 | 用途 |
|------|------|------|
| `start_deploy_api.bat` | 批处理启动脚本 | 简单的前台运行 |
| `start_deploy_api.ps1` | PowerShell 启动脚本 | 支持多种运行模式 |
| `service_daemon.py` | Python 守护进程 | 自动重启和监控 |
| `install_service.bat` | 服务安装脚本 | 安装为 Windows 服务 |
| `uninstall_service.bat` | 服务卸载脚本 | 卸载 Windows 服务 |

## 🎯 各种方式对比

| 方式 | 开机自启 | 自动重启 | 后台运行 | 难度 | 推荐场景 |
|------|---------|---------|---------|------|---------|
| BAT 脚本 | ❌ | ❌ | ❌ | ⭐ | 测试开发 |
| PowerShell | ❌ | ✅ | ✅ | ⭐⭐ | 临时运行 |
| Python 守护 | ❌ | ✅ | ❌ | ⭐⭐ | 开发调试 |
| Windows 服务 | ✅ | ✅ | ✅ | ⭐⭐⭐ | 生产环境 |

## 🛠️ 常见问题

### 1. PowerShell 脚本无法运行

**错误信息:**
```
无法加载文件，因为在此系统上禁止运行脚本
```

**解决方案:**
以管理员身份运行 PowerShell，执行：
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. 端口 8001 被占用

**解决方案 1:** 修改端口
编辑 `deploy_api.py`，修改：
```python
uvicorn.run(
    "deploy_api:app",
    host="0.0.0.0",
    port=8002,  # 改为其他端口
    reload=True,
    log_level="info"
)
```

**解决方案 2:** 关闭占用端口的进程
```bash
# 查找占用端口的进程
netstat -ano | findstr :8001

# 结束进程（PID 为查到的进程ID）
taskkill /PID <PID> /F
```

### 3. 服务安装失败

**可能原因:**
- 没有管理员权限
- 未下载 NSSM
- Python 路径不正确

**解决方案:**
1. 确保以管理员身份运行
2. 下载并放置 nssm.exe
3. 检查 Python 是否在 PATH 中

### 4. 防火墙阻止访问

**解决方案:**
添加防火墙规则：
```bash
# 以管理员身份运行 PowerShell
New-NetFirewallRule -DisplayName "Naver API" -Direction Inbound -LocalPort 8001 -Protocol TCP -Action Allow
```

## 📊 日志查看

### 方式 1: 控制台输出
前台运行模式会直接在控制台显示日志。

### 方式 2: 日志文件（Windows 服务）
```
deploy_code/logs/service.log       # 标准输出日志
deploy_code/logs/service_error.log # 错误日志
```

### 方式 3: Windows 事件查看器
1. 运行 `eventvwr.msc`
2. Windows 日志 → 应用程序
3. 查找来源为 "NaverCommerceAPI" 的事件

## 🔒 安全建议

1. **使用 HTTPS**
   - 在生产环境中使用 Nginx 或 IIS 反向代理
   - 配置 SSL 证书

2. **访问控制**
   - 配置防火墙规则
   - 限制访问 IP 范围
   - 使用 API 密钥认证

3. **日志管理**
   - 定期清理日志文件
   - 设置日志轮转
   - 监控异常访问

## 🚀 生产环境部署建议

### 推荐配置

1. **使用 Windows 服务方式部署**
   ```bash
   # 以管理员身份运行
   install_service.bat
   ```

2. **配置反向代理**
   使用 IIS 或 Nginx 作为反向代理：
   - 提供 HTTPS 支持
   - 负载均衡
   - 静态文件服务

3. **监控和日志**
   - 配置日志轮转
   - 设置告警通知
   - 定期检查服务状态

4. **备份和恢复**
   - 定期备份配置文件
   - 记录部署步骤
   - 准备回滚方案

### 性能优化

编辑 `deploy_api.py`，调整 workers 数量：
```python
uvicorn.run(
    "deploy_api:app",
    host="0.0.0.0",
    port=8001,
    workers=4,  # 根据 CPU 核心数调整
    log_level="info"
)
```

## 📞 技术支持

如有问题，请查看：
- [README.md](README.md) - 基础文档
- [PARAMS_GUIDE.md](PARAMS_GUIDE.md) - 参数说明
- [CHANGELOG.md](CHANGELOG.md) - 更新日志
- [NSSM_GUIDE.md](NSSM_GUIDE.md) - NSSM 详细使用指南 ⭐
- [WINDOWS11_NOTES.md](WINDOWS11_NOTES.md) - Windows 11 特定注意事项 ⭐
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 快速参考手册

## 📝 快速命令参考

```bash
# 测试服务
curl http://localhost:8001/health

# 查看 API 文档
start http://localhost:8001/docs

# 停止服务（如果是前台运行）
Ctrl + C

# 查看进程
tasklist | findstr python

# 结束进程
taskkill /IM python.exe /F

# 查看端口占用
netstat -ano | findstr :8001
```

## 🎉 完成

现在你的服务应该已经在 Windows 上成功运行了！

访问 http://localhost:8001/docs 查看 API 文档。
