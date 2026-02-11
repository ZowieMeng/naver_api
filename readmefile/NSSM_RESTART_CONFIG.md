# NSSM 自动重启配置说明

## 🔄 重启机制说明

### API 更新接口 + NSSM 的完美配合

```
┌─────────────────┐
│ 1. API 收到请求  │
│   /api/deploy/  │
│   update        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 2. 更新代码     │
│   git pull      │
│   pip install   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. 发送退出信号 │
│   SIGTERM       │
│   (延迟2秒)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 4. Python 进程  │
│   退出          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 5. NSSM 检测    │
│   进程退出      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 6. NSSM 自动    │
│   重启服务      │
│   (延迟2秒)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 7. 新代码生效   │
│   服务恢复运行  │
└─────────────────┘
```

---

## ⚙️ 关键配置

### 必须配置（已在 install_service.bat 中自动配置）

```batch
REM 设置进程退出时自动重启
nssm set NaverCommerceAPI AppExit Default Restart

REM 设置重启延迟（毫秒）
nssm set NaverCommerceAPI AppRestartDelay 2000
```

### 配置说明

| 配置项 | 值 | 说明 |
|--------|-----|------|
| `AppExit Default` | `Restart` | 当程序以任何退出码退出时，执行重启操作 |
| `AppRestartDelay` | `2000` | 重启前等待 2000 毫秒（2秒） |

---

## 🔍 验证配置

### 方法一：使用 NSSM 命令

```batch
REM 查看退出策略
nssm get NaverCommerceAPI AppExit

REM 预期输出
Default  Restart
```

```batch
REM 查看重启延迟
nssm get NaverCommerceAPI AppRestartDelay

REM 预期输出
2000
```

### 方法二：使用 NSSM GUI

```batch
REM 打开 NSSM 图形界面
nssm edit NaverCommerceAPI
```

在 "Exit actions" 标签页查看：
- **Default** → **Restart application**
- **Delay restart by** → **2000 milliseconds**

---

## 🛠️ 手动配置（如果之前未配置）

### 如果你之前已经安装了服务但没有配置自动重启：

```batch
REM 1. 添加自动重启配置
nssm set NaverCommerceAPI AppExit Default Restart
nssm set NaverCommerceAPI AppRestartDelay 2000

REM 2. 重启服务使配置生效
nssm restart NaverCommerceAPI

REM 3. 验证配置
nssm get NaverCommerceAPI AppExit
```

---

## 🧪 测试重启功能

### 测试步骤

#### 1. 启动服务
```batch
nssm start NaverCommerceAPI
```

#### 2. 调用更新接口
```bash
curl -X POST http://localhost:8001/api/deploy/update \
  -H "Content-Type: application/json" \
  -d '{"secret_key": "naver_deploy_2026", "install_dependencies": false, "restart_service": true}'
```

或使用测试脚本：
```bash
python test_deploy_update.py --no-deps
```

#### 3. 观察服务状态

```batch
REM 查看服务状态
nssm status NaverCommerceAPI

REM 预期流程：
REM - 服务状态变为 SERVICE_RUNNING
REM - 约 2-4 秒后，服务会短暂退出
REM - NSSM 自动重新启动服务
REM - 服务状态恢复为 SERVICE_RUNNING
```

#### 4. 检查日志

```batch
REM 查看服务日志
type logs\service.log

REM 应该看到类似的输出：
REM [时间] 服务正常运行...
REM [时间] 收到更新请求...
REM [时间] 服务即将重启...
REM [时间] === 服务重新启动 ===
REM [时间] 使用新代码运行...
```

---

## 🚨 常见问题

### Q1: 服务重启后无法启动？

**原因：** 代码可能有语法错误或依赖缺失

**解决方案：**
```batch
REM 1. 查看错误日志
type logs\service_error.log

REM 2. 手动测试启动
cd C:\path\to\project\deploy_code\main
python deploy_api.py

REM 3. 如果有错误，修复后重启服务
nssm restart NaverCommerceAPI
```

### Q2: 重启延迟太短，来不及返回响应？

**当前配置：**
- API 延迟 2 秒后发送 SIGTERM
- NSSM 延迟 2 秒后重启
- 总共约 4 秒完成重启

**如果需要调整：**
```batch
REM 增加重启延迟到 5 秒
nssm set NaverCommerceAPI AppRestartDelay 5000
```

### Q3: 想要禁用自动重启（测试场景）？

```batch
REM 临时禁用自动重启
nssm set NaverCommerceAPI AppExit Default Stop

REM 恢复自动重启
nssm set NaverCommerceAPI AppExit Default Restart
```

### Q4: 如何查看重启历史？

```batch
REM 查看 Windows 事件日志
eventvwr.msc

REM 导航到：
REM Windows 日志 → 系统
REM 筛选事件源: Service Control Manager
REM 查找 NaverCommerceAPI 相关事件
```

---

## 📊 退出策略对比

### NSSM 支持的退出策略

| 策略 | 说明 | 适用场景 |
|------|------|----------|
| `Restart` | 自动重启应用程序 | ✅ 生产环境（推荐） |
| `Ignore` | 不执行任何操作，服务状态保持运行 | 短暂任务 |
| `Exit` | 停止服务 | 维护模式 |
| `Suicide` | 强制终止服务进程 | 调试场景 |

### 我们的配置

```batch
nssm set NaverCommerceAPI AppExit Default Restart
```

- **Default**: 适用于所有退出码
- **Restart**: 自动重启

**也可以针对特定退出码配置：**
```batch
REM 退出码 0 时不重启（正常退出）
nssm set NaverCommerceAPI AppExit 0 Exit

REM 退出码 1 时重启（异常退出）
nssm set NaverCommerceAPI AppExit 1 Restart

REM 其他退出码默认重启
nssm set NaverCommerceAPI AppExit Default Restart
```

---

## 🎯 最佳实践

### 1. 生产环境配置

```batch
REM 自动重启
nssm set NaverCommerceAPI AppExit Default Restart

REM 适当的重启延迟
nssm set NaverCommerceAPI AppRestartDelay 2000

REM 设置重启节流（可选，防止重启风暴）
nssm set NaverCommerceAPI AppThrottle 60000  # 60秒内最多重启一次
```

### 2. 监控和告警

```batch
REM 配置日志
nssm set NaverCommerceAPI AppStdout "%CD%\logs\service.log"
nssm set NaverCommerceAPI AppStderr "%CD%\logs\service_error.log"

REM 启用日志轮转
nssm set NaverCommerceAPI AppRotateFiles 1
nssm set NaverCommerceAPI AppRotateSeconds 86400  # 每天轮转
```

### 3. 渐进式部署

```batch
REM 1. 在测试环境先测试更新
curl http://test-server:8001/api/deploy/update ...

REM 2. 验证服务正常
curl http://test-server:8001/health

REM 3. 再应用到生产环境
curl http://prod-server:8001/api/deploy/update ...
```

---

## 📚 相关文档

- [install_service.bat](install_service.bat) - 服务安装脚本（已包含自动重启配置）
- [NSSM_GUIDE.md](NSSM_GUIDE.md) - NSSM 完整使用指南
- [DEPLOY_UPDATE_GUIDE.md](../../DEPLOY_UPDATE_GUIDE.md) - 更新接口使用指南
- [WINDOWS_DEPLOY.md](WINDOWS_DEPLOY.md) - Windows 部署指南

---

## ✅ 检查清单

在使用更新接口前，请确认：

- [ ] 已使用 `install_service.bat` 安装服务（自动配置重启）
- [ ] 或手动配置了 `AppExit Default Restart`
- [ ] 验证配置：`nssm get NaverCommerceAPI AppExit`
- [ ] 测试手动重启：`nssm restart NaverCommerceAPI`
- [ ] 确认日志目录存在且有写入权限
- [ ] 测试更新接口并观察服务自动重启

---

**版本**: 2.0.0  
**最后更新**: 2026-02-11  
**状态**: ✅ 已在 install_service.bat 中自动配置
