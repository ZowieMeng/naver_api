# 📚 文档导航

快速找到你需要的文档！

## 🚀 快速开始

| 你想做什么？ | 查看这个文档 |
|------------|-------------|
| 快速了解项目 | [README.md](README.md) |
| 在 Windows 上部署 | [WINDOWS_DEPLOY.md](WINDOWS_DEPLOY.md) ⭐ |
| 在 Windows 11 上部署 | [WINDOWS11_NOTES.md](WINDOWS11_NOTES.md) ⭐ |
| 使用图形化启动器 | 双击 `launcher.bat` |
| 查看常用命令 | [QUICK_REFERENCE.md](QUICK_REFERENCE.md) |

## 📖 按主题查找

### Windows 部署

| 文档 | 内容 | 推荐指数 |
|------|------|---------|
| [WINDOWS_DEPLOY.md](WINDOWS_DEPLOY.md) | Windows 完整部署指南 | ⭐⭐⭐⭐⭐ |
| [WINDOWS11_NOTES.md](WINDOWS11_NOTES.md) | Windows 11 特定说明 | ⭐⭐⭐⭐⭐ |
| [NSSM_GUIDE.md](NSSM_GUIDE.md) | NSSM 服务管理详解 | ⭐⭐⭐⭐ |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | 快速命令参考 | ⭐⭐⭐⭐ |

### API 使用

| 文档 | 内容 | 推荐指数 |
|------|------|---------|
| [README.md](README.md) | 基础功能和使用 | ⭐⭐⭐⭐⭐ |
| [PARAMS_GUIDE.md](PARAMS_GUIDE.md) | API 参数详细说明 | ⭐⭐⭐⭐⭐ |
| [CHANGELOG.md](CHANGELOG.md) | 版本更新历史 | ⭐⭐⭐ |

### 示例代码

| 文件 | 内容 | 推荐指数 |
|------|------|---------|
| [usage_examples.py](usage_examples.py) | 完整使用示例 | ⭐⭐⭐⭐⭐ |
| [test_deploy_api.py](test_deploy_api.py) | 测试脚本 | ⭐⭐⭐⭐ |
| [params_builder.py](params_builder.py) | 参数构建工具 | ⭐⭐⭐⭐ |

## 🎯 按场景查找

### 场景 1：我是新手，第一次使用

**推荐阅读顺序：**
1. [README.md](README.md) - 了解项目
2. [WINDOWS_DEPLOY.md](WINDOWS_DEPLOY.md) - Windows 部署
3. 双击 `launcher.bat` - 图形化启动
4. 访问 http://localhost:8001/docs - 查看 API 文档

### 场景 2：我想在 Windows 11 上部署

**推荐阅读顺序：**
1. [WINDOWS11_NOTES.md](WINDOWS11_NOTES.md) - Windows 11 注意事项
2. [NSSM_GUIDE.md](NSSM_GUIDE.md) - NSSM 兼容性确认
3. 双击 `launcher.bat` → 选择 [4] 安装服务
4. [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 常用命令

### 场景 3：我想了解 API 参数

**推荐阅读顺序：**
1. [PARAMS_GUIDE.md](PARAMS_GUIDE.md) - 参数详细说明
2. [params_builder.py](params_builder.py) - 参数构建工具
3. [usage_examples.py](usage_examples.py) - 实际使用示例
4. 访问 http://localhost:8001/docs - 交互式文档

### 场景 4：遇到问题需要排查

**推荐查看：**
1. [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 故障排除部分
2. [WINDOWS11_NOTES.md](WINDOWS11_NOTES.md) - Win11 特定问题
3. [NSSM_GUIDE.md](NSSM_GUIDE.md) - NSSM 故障排查
4. [WINDOWS_DEPLOY.md](WINDOWS_DEPLOY.md) - 常见问题部分

### 场景 5：我想部署到生产环境

**推荐阅读顺序：**
1. [WINDOWS_DEPLOY.md](WINDOWS_DEPLOY.md) - 生产环境部署
2. [NSSM_GUIDE.md](NSSM_GUIDE.md) - Windows 服务配置
3. [WINDOWS11_NOTES.md](WINDOWS11_NOTES.md) - 性能优化
4. [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 服务管理命令

### 场景 6：我想了解 API 的变更

**推荐查看：**
1. [CHANGELOG.md](CHANGELOG.md) - 版本更新历史
2. [PARAMS_GUIDE.md](PARAMS_GUIDE.md) - 新参数说明
3. [verify_new_api.py](verify_new_api.py) - 验证新功能

## 🔍 按关键词查找

### NSSM / Windows 服务
- [NSSM_GUIDE.md](NSSM_GUIDE.md) - 完整指南
- [WINDOWS_DEPLOY.md](WINDOWS_DEPLOY.md) - 第4章节
- [install_service.bat](install_service.bat) - 安装脚本

### Windows 11
- [WINDOWS11_NOTES.md](WINDOWS11_NOTES.md) - 专门文档
- [NSSM_GUIDE.md](NSSM_GUIDE.md) - 兼容性说明
- [WINDOWS_DEPLOY.md](WINDOWS_DEPLOY.md) - 兼容性部分

### API 参数 / params
- [PARAMS_GUIDE.md](PARAMS_GUIDE.md) - 详细文档
- [params_builder.py](params_builder.py) - 工具函数
- [CHANGELOG.md](CHANGELOG.md) - v2.0.0 变更说明

### 启动 / 运行
- [launcher.bat](launcher.bat) - 图形化启动器
- [start_deploy_api.bat](start_deploy_api.bat) - 批处理
- [start_deploy_api.ps1](start_deploy_api.ps1) - PowerShell
- [service_daemon.py](service_daemon.py) - 守护进程

### 测试 / 示例
- [test_deploy_api.py](test_deploy_api.py) - 测试脚本
- [usage_examples.py](usage_examples.py) - 使用示例
- [verify_new_api.py](verify_new_api.py) - API 验证

## 📂 完整文件列表

### 📄 文档文件

| 文件名 | 说明 | 页数 |
|--------|------|------|
| README.md | 项目主文档 | ~200行 |
| WINDOWS_DEPLOY.md | Windows 部署指南 | ~400行 |
| WINDOWS11_NOTES.md | Windows 11 注意事项 | ~350行 |
| NSSM_GUIDE.md | NSSM 使用指南 | ~450行 |
| PARAMS_GUIDE.md | 参数详细说明 | ~350行 |
| QUICK_REFERENCE.md | 快速参考 | ~200行 |
| CHANGELOG.md | 更新日志 | ~150行 |
| DOCS_NAVIGATION.md | 本文档 | ~150行 |

### 🐍 Python 文件

| 文件名 | 说明 | 行数 |
|--------|------|------|
| deploy_api.py | FastAPI 主服务 | ~340行 |
| setp_function_code.py | 业务逻辑 | ~300行 |
| params_builder.py | 参数构建工具 | ~200行 |
| service_daemon.py | 守护进程 | ~150行 |
| test_deploy_api.py | 测试脚本 | ~200行 |
| usage_examples.py | 使用示例 | ~250行 |
| verify_new_api.py | API 验证 | ~100行 |

### 🖥️ Windows 脚本

| 文件名 | 说明 | 类型 |
|--------|------|------|
| launcher.bat | 图形化启动器 | BAT |
| start_deploy_api.bat | 简单启动 | BAT |
| start_deploy_api.ps1 | 多模式启动 | PS1 |
| install_service.bat | 服务安装 | BAT |
| uninstall_service.bat | 服务卸载 | BAT |

### 🐧 Linux/macOS 脚本

| 文件名 | 说明 | 类型 |
|--------|------|------|
| start_deploy_api.sh | Shell 启动脚本 | SH |

## 💡 使用技巧

### 技巧 1：使用图形化启动器

最简单的方式 - 双击 `launcher.bat`，所有功能一目了然！

### 技巧 2：快速搜索

在文档中按 `Ctrl+F` 搜索关键词：
- 搜索 "Windows 11" 查看兼容性
- 搜索 "NSSM" 查看服务相关
- 搜索 "params" 查看参数相关
- 搜索 "Error" 查看故障排除

### 技巧 3：在线 API 文档

启动服务后访问：
```
http://localhost:8001/docs
```
这是最权威的 API 参考！

### 技巧 4：参数构建工具

不确定参数格式？运行：
```bash
python params_builder.py
```
查看各种示例！

### 技巧 5：快速测试

想测试功能？运行：
```bash
python test_deploy_api.py
```
自动测试所有端点！

## 🆘 还是找不到？

### 查看在线文档
启动服务后访问：http://localhost:8001/docs

### 运行示例代码
```bash
python usage_examples.py
```

### 查看快速参考
[QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 最常用的命令都在这里

### 使用图形化工具
```bash
launcher.bat → 选择 [6] 查看服务状态
```

## 📊 文档质量

| 文档 | 完整度 | 准确度 | 易读性 | 更新频率 |
|------|--------|--------|--------|---------|
| README.md | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 高 |
| WINDOWS_DEPLOY.md | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 高 |
| WINDOWS11_NOTES.md | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 中 |
| NSSM_GUIDE.md | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 中 |
| PARAMS_GUIDE.md | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 高 |
| QUICK_REFERENCE.md | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 中 |

---

**建议：** 如果是第一次使用，从 [README.md](README.md) 开始！
