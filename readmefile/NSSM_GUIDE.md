# NSSM 详细使用指南

## 什么是 NSSM？

NSSM (Non-Sucking Service Manager) 是一个免费、开源的 Windows 服务管理工具，可以将任何程序安装为 Windows 服务。

**官方网站：** https://nssm.cc/

## ✅ Windows 11 兼容性确认

### 完全兼容

NSSM **完全兼容 Windows 11**，包括：
- ✅ Windows 11 Home
- ✅ Windows 11 Pro
- ✅ Windows 11 Enterprise
- ✅ Windows 11 Education

### 版本兼容性

| Windows 版本 | NSSM 兼容性 | 备注 |
|-------------|------------|------|
| Windows 11 | ✅ 完全兼容 | 已在多个环境测试 |
| Windows 10 | ✅ 完全兼容 | 长期稳定使用 |
| Windows 8.1 | ✅ 完全兼容 | |
| Windows 8 | ✅ 完全兼容 | |
| Windows 7 | ✅ 完全兼容 | |
| Windows Server 2022 | ✅ 完全兼容 | |
| Windows Server 2019 | ✅ 完全兼容 | |
| Windows Server 2016 | ✅ 完全兼容 | |
| Windows Server 2012/R2 | ✅ 完全兼容 | |

## 📥 下载和安装

### 1. 下载 NSSM

```
官方下载地址: https://nssm.cc/download
```

**推荐版本：** NSSM 2.24（最新稳定版）

### 2. 选择正确的版本

下载后解压，你会看到两个文件夹：

```
nssm-2.24/
├── win32/
│   └── nssm.exe    ← 32位系统使用
└── win64/
    └── nssm.exe    ← 64位系统使用（推荐）
```

**如何确定系统位数：**

**方法 1：** 按 `Win + Pause` 键，查看"系统类型"
**方法 2：** 运行以下命令：
```cmd
wmic os get osarchitecture
```

### 3. 安装 NSSM

**选项 A：复制到项目目录（推荐）**
```
将 nssm.exe 复制到 deploy_code 目录
```

**选项 B：添加到系统 PATH**
```
1. 复制 nssm.exe 到 C:\Windows\System32\
2. 或添加 nssm.exe 所在目录到 PATH 环境变量
```

## 🚀 使用 NSSM

### 自动安装（推荐）

```bash
# 右键"以管理员身份运行"
install_service.bat
```

### 手动安装

#### 1. 使用 GUI 界面

```bash
# 以管理员身份运行
nssm install NaverCommerceAPI
```

这会打开图形界面：
1. **Application**
   - Path: `C:\Python310\python.exe`（你的 Python 路径）
   - Startup directory: `C:\path\to\deploy_code`
   - Arguments: `deploy_api.py`

2. **Details**
   - Display name: `Naver Commerce Deploy API`
   - Description: `Naver 商城部署服务`
   - Startup type: `Automatic`

3. **Log on**
   - 使用默认的 Local System account

4. **I/O**
   - Output (stdout): `logs\service.log`
   - Error (stderr): `logs\service_error.log`

5. 点击 "Install service"

#### 2. 使用命令行

```bash
# 以管理员身份运行 PowerShell 或 CMD

# 获取 Python 路径
python -c "import sys; print(sys.executable)"

# 安装服务
nssm install NaverCommerceAPI "C:\Python310\python.exe" "C:\path\to\deploy_code\deploy_api.py"

# 设置工作目录
nssm set NaverCommerceAPI AppDirectory "C:\path\to\deploy_code"

# 设置显示名称
nssm set NaverCommerceAPI DisplayName "Naver Commerce Deploy API"

# 设置描述
nssm set NaverCommerceAPI Description "Naver 商城部署服务 - 订单查询与发货管理"

# 设置自动启动
nssm set NaverCommerceAPI Start SERVICE_AUTO_START

# 设置日志
nssm set NaverCommerceAPI AppStdout "C:\path\to\deploy_code\logs\service.log"
nssm set NaverCommerceAPI AppStderr "C:\path\to\deploy_code\logs\service_error.log"
nssm set NaverCommerceAPI AppRotateFiles 1
nssm set NaverCommerceAPI AppRotateSeconds 86400

# 启动服务
nssm start NaverCommerceAPI
```

## 🔧 服务管理命令

### 基本操作

```bash
# 启动服务
nssm start NaverCommerceAPI

# 停止服务
nssm stop NaverCommerceAPI

# 重启服务
nssm restart NaverCommerceAPI

# 查看服务状态
nssm status NaverCommerceAPI
```

### 服务配置

```bash
# 编辑服务（打开 GUI）
nssm edit NaverCommerceAPI

# 查看服务配置
nssm get NaverCommerceAPI <parameter>

# 设置服务配置
nssm set NaverCommerceAPI <parameter> <value>

# 重置服务配置
nssm reset NaverCommerceAPI <parameter>
```

### 删除服务

```bash
# 停止并删除服务
nssm stop NaverCommerceAPI
nssm remove NaverCommerceAPI confirm

# 或使用脚本
uninstall_service.bat
```

## 🎯 常用配置参数

| 参数 | 说明 | 示例 |
|------|------|------|
| AppDirectory | 工作目录 | `nssm set NaverCommerceAPI AppDirectory "C:\path"` |
| DisplayName | 显示名称 | `nssm set NaverCommerceAPI DisplayName "我的服务"` |
| Description | 服务描述 | `nssm set NaverCommerceAPI Description "描述文字"` |
| Start | 启动类型 | `nssm set NaverCommerceAPI Start SERVICE_AUTO_START` |
| AppStdout | 标准输出 | `nssm set NaverCommerceAPI AppStdout "logs\out.log"` |
| AppStderr | 错误输出 | `nssm set NaverCommerceAPI AppStderr "logs\err.log"` |
| AppRotateFiles | 日志轮转 | `nssm set NaverCommerceAPI AppRotateFiles 1` |
| AppRotateSeconds | 轮转间隔 | `nssm set NaverCommerceAPI AppRotateSeconds 86400` |

## 🔍 故障排查

### 问题 1：服务无法启动

**检查步骤：**
```bash
# 1. 查看服务状态
nssm status NaverCommerceAPI

# 2. 查看日志
type logs\service_error.log

# 3. 手动测试
python deploy_api.py

# 4. 检查 Python 路径
nssm get NaverCommerceAPI Application
```

**常见原因：**
- Python 路径不正确
- 工作目录设置错误
- 缺少依赖包
- 端口被占用

### 问题 2：服务安装失败

**解决方案：**
```bash
# 1. 确保以管理员身份运行
# 2. 删除已存在的服务
nssm remove NaverCommerceAPI confirm

# 3. 重新安装
install_service.bat
```

### 问题 3：日志文件未创建

**解决方案：**
```bash
# 创建日志目录
mkdir logs

# 设置日志路径（使用绝对路径）
nssm set NaverCommerceAPI AppStdout "C:\path\to\deploy_code\logs\service.log"
nssm set NaverCommerceAPI AppStderr "C:\path\to\deploy_code\logs\service_error.log"
```

### 问题 4：Windows 11 SmartScreen 警告

**解决方案：**
1. 点击"更多信息"
2. 点击"仍要运行"
3. 或在文件属性中"解除锁定"

### 问题 5：服务频繁重启

**检查原因：**
```bash
# 查看错误日志
type logs\service_error.log

# 查看事件查看器
eventvwr.msc
→ Windows 日志 → 应用程序
→ 查找来源为 NaverCommerceAPI 的事件
```

## 🔐 Windows 11 特定注意事项

### 1. UAC（用户账户控制）

Windows 11 的 UAC 更严格，确保：
- 以管理员身份运行所有安装命令
- 右键选择"以管理员身份运行"

### 2. Windows Defender

如果被 Windows Defender 阻止：
```
设置 → 隐私和安全性 → Windows 安全中心 → 病毒和威胁防护
→ 管理设置 → 排除项 → 添加或移除排除项
→ 添加 nssm.exe 和 deploy_code 目录
```

### 3. 防火墙

确保端口 8001 已开放：
```powershell
# 以管理员身份运行 PowerShell
New-NetFirewallRule -DisplayName "Naver API" -Direction Inbound -LocalPort 8001 -Protocol TCP -Action Allow
```

## 📊 在 Windows 服务管理器中管理

### 打开服务管理器

```bash
# 方法 1: 运行命令
services.msc

# 方法 2: 任务管理器
Ctrl + Shift + Esc → 服务标签页

# 方法 3: 计算机管理
compmgmt.msc → 服务和应用程序 → 服务
```

### 在服务管理器中操作

找到 "Naver Commerce Deploy API"，可以：
- 启动/停止/重启服务
- 设置启动类型（自动/手动/禁用）
- 查看服务状态
- 配置恢复选项

## 📚 高级用法

### 环境变量

```bash
# 设置环境变量
nssm set NaverCommerceAPI AppEnvironmentExtra "API_ENV=production" "DEBUG=false"
```

### 进程优先级

```bash
# 设置为高优先级
nssm set NaverCommerceAPI AppPriority ABOVE_NORMAL_PRIORITY_CLASS
```

### 依赖服务

```bash
# 设置依赖（例如依赖网络服务）
nssm set NaverCommerceAPI DependOnService LanmanServer
```

### 自动恢复

```bash
# 配置服务失败后自动重启
nssm set NaverCommerceAPI AppExit Default Restart
nssm set NaverCommerceAPI AppRestartDelay 5000
```

## 🎉 验证安装

### 检查服务状态

```bash
# 使用 NSSM
nssm status NaverCommerceAPI

# 使用 Windows 命令
sc query NaverCommerceAPI

# 或访问服务
curl http://localhost:8001/health
```

### 查看日志

```bash
# 标准输出日志
type logs\service.log

# 错误日志
type logs\service_error.log

# 实时查看日志（PowerShell）
Get-Content logs\service.log -Wait
```

## 📞 获取帮助

### NSSM 帮助

```bash
# 查看帮助
nssm help

# 查看特定命令帮助
nssm help install
nssm help set
```

### 相关文档

- **NSSM 官方文档**: https://nssm.cc/usage
- **Windows 部署指南**: [WINDOWS_DEPLOY.md](WINDOWS_DEPLOY.md)
- **快速参考**: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

## ✅ 总结

NSSM 是将 Python 应用部署为 Windows 服务的最佳方案：

- ✅ **完全兼容 Windows 11**
- ✅ 简单易用，图形界面和命令行双支持
- ✅ 功能强大，配置灵活
- ✅ 开源免费，社区活跃
- ✅ 稳定可靠，广泛使用

**推荐用于生产环境！**
