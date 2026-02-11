# Naver Commerce Deploy API 服务

基于 FastAPI 构建的 Naver 商城部署服务接口，提供订单查询和发货状态上传功能。

## 📋 功能特性

- ✅ **获取访问令牌** - 自动生成 Naver Commerce API 访问令牌
- ✅ **查询已付款订单** - 获取指定时间范围内的已付款订单列表
- ✅ **上传发货状态** - 批量上传订单发货信息到 Naver Commerce
- ✅ **自动化文档** - 提供 Swagger UI 和 ReDoc 交互式文档
- ✅ **错误处理** - 完整的错误处理和响应机制

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install fastapi uvicorn pydantic requests bcrypt pybase64 pytz
```

或使用 requirements.txt：

```bash
pip install -r ../requirements.txt
```

### 2. 启动服务

#### Linux / macOS

**方式一：使用启动脚本（推荐）**

```bash
./start_deploy_api.sh
```

**方式二：直接运行**

```bash
python deploy_api.py
```

#### Windows

**方式一：批处理脚本（最简单）**

双击运行 `start_deploy_api.bat`

**方式二：PowerShell 脚本（推荐）**

右键运行 `start_deploy_api.ps1` → "使用 PowerShell 运行"

支持三种模式：前台运行、后台运行、守护模式（自动重启）

**方式三：Python 守护进程**

```bash
python service_daemon.py
```

**方式四：安装为 Windows 服务**

右键"以管理员身份运行" `install_service.bat`

> **Windows 11 兼容性：** ✅ NSSM 完全支持 Windows 11/10/8/7  
> 详细的 Windows 部署指南请查看 [WINDOWS_DEPLOY.md](WINDOWS_DEPLOY.md)  
> NSSM 详细使用说明请查看 [NSSM_GUIDE.md](NSSM_GUIDE.md)

---

服务将在 `http://0.0.0.0:8001` 启动

### 3. 访问文档

- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc
- **健康检查**: http://localhost:8001/health

## 📡 API 端点

### 1. 获取访问令牌

**POST** `/api/token`

自动生成并获取 Naver Commerce API 访问令牌。

**请求参数（Query）:**
```
- client_id (可选): 客户端 ID
- client_secret (可选): 客户端密钥
```

**响应示例:**
```json
{
  "success": true,
  "access_token": "AAAAOHxxxxxxxxxxxxxxxxxxxxxxxxxxxxxCOA",
  "expires_in": 3600,
  "token_type": "Bearer",
  "message": "Token 获取成功"
}
```

**cURL 示例:**
```bash
curl -X POST "http://localhost:8001/api/token"
```

---

### 2. 获取已付款订单

**POST** `/api/orders/payed`

查询指定参数的已付款订单列表。

**请求体（JSON）:**
```json
{
  "access_token": "YOUR_ACCESS_TOKEN",
  "params": {
    "from": "2024-02-10T00:00:00.000+09:00",
    "to": "2024-02-11T23:59:59.999+09:00",
    "productOrderStatuses": ["PAYED"],
    "placeOrderStatusType": "OK",
    "fulfillment": false,
    "pageSize": 100,
    "page": 1
  }
}
```

**字段说明:**
- `access_token`: API 访问令牌（必填）
- `params`: 查询参数字典（必填）
  - `from`: 开始时间（ISO 8601 格式）
  - `to`: 结束时间（ISO 8601 格式）
  - `productOrderStatuses`: 订单状态列表（如 ["PAYED"]）
  - `placeOrderStatusType`: 订单类型（如 "OK"）
  - `fulfillment`: 是否使用物流服务（布尔值）
  - `pageSize`: 每页数量（1-100）
  - `page`: 页码

**响应示例:**
```json
{
  "success": true,
  "orders": [
    {
      "productOrderId": "2024021100001",
      "productOrderStatus": "PAYED",
      "orderDate": "2024-02-11T10:30:00+09:00",
      ...
    }
  ],
  "total_count": 5,
  "message": "成功获取 5 条订单"
}
```

**cURL 示例:**
```bash
curl -X POST "http://localhost:8001/api/orders/payed" \
  -H "Content-Type: application/json" \
  -d '{
    "access_token": "YOUR_TOKEN",
    "params": {
      "from": "2024-02-10T00:00:00.000+09:00",
      "to": "2024-02-11T23:59:59.999+09:00",
      "productOrderStatuses": ["PAYED"],
      "placeOrderStatusType": "OK",
      "fulfillment": false,
      "pageSize": 100,
      "page": 1
    }
  }'
```

**Python 示例:**
```python
import requests
from datetime import datetime, timedelta
import pytz

# 1. 获取 token
token_response = requests.post("http://localhost:8001/api/token")
access_token = token_response.json()['access_token']

# 2. 计算日期范围
tz = pytz.timezone('Asia/Seoul')
now = datetime.now(tz)
from_date = now - timedelta(days=1)

# 3. 查询订单
request_data = {
    "access_token": access_token,
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

orders_response = requests.post(
    "http://localhost:8001/api/orders/payed",
    json=request_data
)
orders = orders_response.json()['orders']
print(f"获取到 {len(orders)} 个订单")
```

---

### 3. 上传发货状态

**POST** `/api/orders/dispatch`

批量上传订单的发货信息到 Naver Commerce。

**请求体（JSON）:**
```json
{
  "product_orders": [
    {
      "productOrderId": "2024021100001",
      "deliveryMethod": "DELIVERY",
      "deliveryCompanyCode": "CJGLS",
      "trackingNumber": "1234567890123",
      "dispatchDate": "2024-02-11T15:00:00+09:00"
    }
  ],
  "access_token": "YOUR_ACCESS_TOKEN"
}
```

**字段说明:**
- `productOrderId`: 产品订单 ID（必填）
- `deliveryMethod`: 配送方式，默认 "DELIVERY"
- `deliveryCompanyCode`: 物流公司代码（必填）
- `trackingNumber`: 运单号（必填）
- `dispatchDate`: 发货日期，ISO 8601 格式（可选，不提供则使用当前时间）
- `access_token`: 访问令牌（可选，不提供则自动获取）

**响应示例:**
```json
{
  "success": true,
  "response": {
    "timestamp": "2024-02-11T15:00:00.000+09:00",
    "message": "Success"
  },
  "message": "订单发货状态上传成功"
}
```

**cURL 示例:**
```bash
curl -X POST "http://localhost:8001/api/orders/dispatch" \
  -H "Content-Type: application/json" \
  -d '{
    "product_orders": [
      {
        "productOrderId": "2024021100001",
        "deliveryMethod": "DELIVERY",
        "deliveryCompanyCode": "CJGLS",
        "trackingNumber": "1234567890123"
      }
    ],
    "access_token": "YOUR_ACCESS_TOKEN"
  }'
```

**Python 示例:**
```python
import requests
from datetime import datetime

# 1. 获取 token
token_response = requests.post("http://localhost:8001/api/token")
access_token = token_response.json()['access_token']

# 2. 准备发货数据
dispatch_data = {
    "product_orders": [
        {
            "productOrderId": "2024021100001",
            "deliveryMethod": "DELIVERY",
            "deliveryCompanyCode": "CJGLS",
            "trackingNumber": "1234567890123",
            "dispatchDate": datetime.now().isoformat()
        }
    ],
    "access_token": access_token
}

# 3. 上传发货状态
response = requests.post(
    "http://localhost:8001/api/orders/dispatch",
    json=dispatch_data
)

if response.status_code == 200:
    print("✓ 发货状态上传成功")
else:
    print(f"✗ 上传失败: {response.json()}")
```

---

### 4. 健康检查

**GET** `/` 或 `/health`

检查服务运行状态。

**响应示例:**
```json
{
  "status": "healthy",
  "timestamp": "2024-02-11T15:00:00.000000"
}
```

## 🧪 测试

运行测试脚本测试所有 API 功能：

```bash
python test_deploy_api.py
```

测试脚本会自动：
1. 检查服务健康状态
2. 获取访问令牌
3. 查询已付款订单
4. 测试发货状态上传

## 🏗️ 项目结构

```
deploy_code/
├── setp_function_code.py       # 业务逻辑函数
├── deploy_api.py               # FastAPI 服务主文件
├── params_builder.py           # 参数构建辅助工具
├── service_daemon.py           # Python 守护进程
│
├── start_deploy_api.sh         # Linux/macOS 启动脚本
├── start_deploy_api.bat        # Windows 批处理启动脚本
├── start_deploy_api.ps1        # Windows PowerShell 启动脚本
├── launcher.bat                # Windows 图形化启动器
├── install_service.bat         # Windows 服务安装脚本
├── uninstall_service.bat       # Windows 服务卸载脚本
│
├── test_deploy_api.py          # 测试脚本
├── usage_examples.py           # 使用示例代码
├── verify_new_api.py           # API 验证脚本
│
├── README.md                   # 本文档
├── PARAMS_GUIDE.md             # 参数详细说明文档
├── WINDOWS_DEPLOY.md           # Windows 部署指南
├── WINDOWS11_NOTES.md          # Windows 11 特定注意事项
├── NSSM_GUIDE.md               # NSSM 详细使用指南
├── QUICK_REFERENCE.md          # 快速参考手册
└── CHANGELOG.md                # 更新日志
```

## 📝 配置说明

默认配置在 `setp_function_code.py` 中：

```python
clientId = "3Nu2hAaKhBp1Aj6jo1goP3"
clientSecret = "$2a$04$/HKy4NTQW/nFKpvN5b/Suu"
```

如需使用其他配置，可以在调用 API 时通过参数传入。

## 📚 参数构建工具

项目提供了参数构建辅助工具，简化 API 调用：

- **[PARAMS_GUIDE.md](PARAMS_GUIDE.md)** - 详细的参数说明文档
- **[params_builder.py](params_builder.py)** - 参数构建辅助工具

使用示例：
```python
from params_builder import build_payed_orders_params

# 快速构建查询参数
params = build_payed_orders_params(days=3)
```

## 🔧 常见物流公司代码

| 代码 | 公司名称 |
|------|---------|
| CJGLS | CJ 大韩通运 |
| HANJIN | 韩进快递 |
| LOTTE | 乐天物流 |
| KDEXP | 经东物流 |
| EPOST | 韩国邮政 |

更多物流公司代码请参考：[DELIVERY_CODES.md](../DELIVERY_CODES.md)

## ⚠️ 注意事项

1. **时区处理**: 所有时间默认使用韩国时区 (Asia/Seoul)
2. **Token 有效期**: Access token 一般有效期为 1 小时
3. **订单状态**: 只查询状态为 PAYED 的订单
4. **批量上传**: dispatch 接口支持批量上传多个订单
5. **错误处理**: 所有接口都包含详细的错误信息返回

## 🆘 故障排除

### 问题：服务无法启动

**解决方案:**
```bash
# 检查端口 8001 是否被占用
lsof -i :8001

# 如果被占用，杀死进程或更改端口
# 在 deploy_api.py 中修改 port=8001 为其他端口
```

### 问题：Token 获取失败

**解决方案:**
- 检查 clientId 和 clientSecret 配置是否正确
- 确认网络连接正常
- 查看详细错误信息

### 问题：订单查询返回空列表

**解决方案:**
- 确认指定时间范围内有已付款订单
- 检查 access_token 是否有效
- 调整 params 中的 from 和 to 日期范围查询更长时间
- 确认 params 参数格式正确

## 📞 联系与支持

如有问题或建议，请参考：
- API 文档: http://localhost:8001/docs
- 错误代码说明: [API_GUIDE.md](../API_GUIDE.md)
- 物流代码列表: [DELIVERY_CODES.md](../DELIVERY_CODES.md)

## 📄 许可证

本项目仅供内部使用。
