# 更新日志 (CHANGELOG)

## [2.0.0] - 2026-02-11

### 重大变更 (Breaking Changes)

#### `/api/orders/payed` 接口参数变更

**变更内容:**
- 从 Query 参数改为 JSON Body 请求
- `days` 参数改为灵活的 `params` 字典

**之前的调用方式:**
```python
# 旧版本 (已废弃)
params = {"access_token": "xxx", "days": 1}
response = requests.post(
    "http://localhost:8001/api/orders/payed",
    params=params  # Query 参数
)
```

**新的调用方式:**
```python
# 新版本 (推荐)
request_data = {
    "access_token": "xxx",
    "params": {
        "from": "2024-02-10T00:00:00.000+09:00",
        "to": "2024-02-11T23:59:59.999+09:00",
        "productOrderStatuses": ["PAYED"],
        "placeOrderStatusType": "OK",
        "fulfillment": False,
        "pageSize": 100,
        "page": 1
    }
}
response = requests.post(
    "http://localhost:8001/api/orders/payed",
    json=request_data  # JSON Body
)
```

### 新增功能

1. **参数构建辅助工具** (`params_builder.py`)
   - `build_payed_orders_params()` - 快速构建查询参数
   - `build_custom_orders_params()` - 自定义查询参数构建
   - 自动处理日期格式和时区转换

2. **详细参数文档** (`PARAMS_GUIDE.md`)
   - 完整的参数说明
   - 订单状态列表
   - 日期格式规范
   - 常见错误解决方案
   - 多个实用示例

3. **更新的测试脚本**
   - 支持新的参数格式
   - 更完整的测试覆盖

### 优势

✅ **更灵活** - 可以自定义所有查询参数  
✅ **更强大** - 支持多种订单状态、分页等高级查询  
✅ **更清晰** - 参数结构更直观，易于理解  
✅ **更易维护** - 日期计算由调用方控制，职责分离  

### 迁移指南

如果你使用的是旧版本接口，请按照以下步骤迁移：

#### 步骤 1: 导入辅助工具

```python
from params_builder import build_payed_orders_params
```

#### 步骤 2: 修改调用代码

**旧代码:**
```python
params = {"access_token": token, "days": 3}
response = requests.post(url, params=params)
```

**新代码:**
```python
# 使用辅助工具
params_dict = build_payed_orders_params(days=3)
request_data = {"access_token": token, "params": params_dict}
response = requests.post(url, json=request_data)

# 或手动构建
from datetime import datetime, timedelta
import pytz

tz = pytz.timezone('Asia/Seoul')
now = datetime.now(tz)
from_date = now - timedelta(days=3)

request_data = {
    "access_token": token,
    "params": {
        "from": from_date.isoformat(timespec='milliseconds'),
        "to": now.isoformat(timespec='milliseconds'),
        "productOrderStatuses": ["PAYED"],
        "placeOrderStatusType": "OK",
        "fulfillment": False,
        "pageSize": 100,
        "page": 1
    }
}
response = requests.post(url, json=request_data)
```

### 文件变更

#### 修改的文件
- `setp_function_code.py` - `get_payed_orders()` 函数签名变更
- `deploy_api.py` - `/api/orders/payed` 端点实现变更
- `test_deploy_api.py` - 测试用例更新
- `usage_examples.py` - 示例代码更新
- `README.md` - 文档更新

#### 新增的文件
- `params_builder.py` - 参数构建工具
- `PARAMS_GUIDE.md` - 参数详细说明
- `CHANGELOG.md` - 本更新日志

### 向后兼容性

⚠️ **不兼容旧版本** - 此版本包含破坏性变更，无法向后兼容 v1.x

如果需要保持旧版本兼容，建议：
1. 使用分支管理不同版本
2. 或在新版本中添加兼容层

### 已知问题

无

### 未来计划

- [ ] 添加更多订单状态查询支持
- [ ] 支持批量查询优化
- [ ] 添加订单数据缓存机制
- [ ] WebSocket 实时订单推送

---

## [1.0.0] - 2026-02-11

### 首次发布

- ✨ FastAPI 服务框架
- ✨ 获取访问令牌接口
- ✨ 查询已付款订单接口（基于 days 参数）
- ✨ 上传发货状态接口
- ✨ 健康检查接口
- 📚 基础文档
- 🧪 测试脚本
