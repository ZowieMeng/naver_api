# 订单查询参数说明文档

## API 参数详解

### `/api/orders/payed` - 获取已付款订单

该接口使用 POST 方法，接受 JSON 格式的请求体。

## 完整参数结构

```json
{
  "access_token": "访问令牌",
  "params": {
    "from": "开始时间",
    "to": "结束时间",
    "productOrderStatuses": ["订单状态列表"],
    "placeOrderStatusType": "订单类型",
    "fulfillment": false,
    "pageSize": 100,
    "page": 1
  }
}
```

## 参数详细说明

### 顶层参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| access_token | string | 是 | Naver Commerce API 访问令牌 |
| params | object | 是 | 订单查询参数对象 |

### params 对象参数

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| from | string | 是 | 查询开始时间（ISO 8601 格式） | "2024-02-10T00:00:00.000+09:00" |
| to | string | 是 | 查询结束时间（ISO 8601 格式） | "2024-02-11T23:59:59.999+09:00" |
| productOrderStatuses | array | 否 | 订单状态列表 | ["PAYED"] |
| placeOrderStatusType | string | 否 | 订单类型 | "OK" 或 "CANCEL" |
| fulfillment | boolean | 否 | 是否使用物流服务 | false |
| pageSize | integer | 否 | 每页返回数量（1-100） | 100 |
| page | integer | 否 | 页码（从 1 开始） | 1 |

## 订单状态说明

### productOrderStatuses 可选值

| 状态值 | 说明 |
|--------|------|
| PAYED | 已付款 |
| DELIVERING | 配送中 |
| DELIVERED | 已送达 |
| PURCHASE_DECIDED | 购买确认 |
| EXCHANGED | 已换货 |
| CANCELED | 已取消 |
| RETURNED | 已退货 |
| CANCELED_BY_NOPAYMENT | 因未付款取消 |

### placeOrderStatusType 可选值

| 类型 | 说明 |
|------|------|
| OK | 正常订单 |
| CANCEL | 取消订单 |

## 日期时间格式

### ISO 8601 格式规范

订单查询接口要求使用 ISO 8601 格式的日期时间，必须包含：
- 日期和时间
- 毫秒精度
- 时区信息

**格式模板:**
```
YYYY-MM-DDTHH:MM:SS.sss+09:00
```

**示例:**
```
2024-02-11T14:30:00.000+09:00
```

### Python 生成示例

```python
from datetime import datetime
import pytz

# 韩国时区
tz = pytz.timezone('Asia/Seoul')

# 当前时间
now = datetime.now(tz)
now_str = now.isoformat(timespec='milliseconds')
print(now_str)  # 输出: 2024-02-11T14:30:00.000+09:00

# 指定时间
dt = datetime(2024, 2, 11, 0, 0, 0, tzinfo=tz)
dt_str = dt.isoformat(timespec='milliseconds')
print(dt_str)  # 输出: 2024-02-11T00:00:00.000+09:00
```

### JavaScript 生成示例

```javascript
// 当前时间
const now = new Date();
const nowStr = now.toISOString();  // 输出: 2024-02-11T05:30:00.000Z

// 转换为韩国时区格式
const kstOffset = 9 * 60;  // 韩国时区 UTC+9
const kstDate = new Date(now.getTime() + kstOffset * 60 * 1000);
const kstStr = kstDate.toISOString().replace('Z', '+09:00');
```

## 完整请求示例

### 示例 1: 查询最近 24 小时的已付款订单

```python
import requests
from datetime import datetime, timedelta
import pytz

# 获取 token
token_response = requests.post("http://localhost:8001/api/token")
access_token = token_response.json()['access_token']

# 计算时间范围
tz = pytz.timezone('Asia/Seoul')
now = datetime.now(tz)
yesterday = now - timedelta(days=1)

# 构建请求
request_data = {
    "access_token": access_token,
    "params": {
        "from": yesterday.isoformat(timespec='milliseconds'),
        "to": now.isoformat(timespec='milliseconds'),
        "productOrderStatuses": ["PAYED"],
        "placeOrderStatusType": "OK",
        "fulfillment": False,
        "pageSize": 100,
        "page": 1
    }
}

# 发送请求
response = requests.post(
    "http://localhost:8001/api/orders/payed",
    json=request_data
)

# 处理响应
if response.status_code == 200:
    data = response.json()
    orders = data['orders']
    print(f"成功获取 {len(orders)} 个订单")
else:
    print(f"请求失败: {response.status_code}")
```

### 示例 2: 分页查询大量订单

```python
def get_all_payed_orders(access_token, from_date, to_date):
    """分页获取所有订单"""
    all_orders = []
    page = 1
    page_size = 100
    
    while True:
        request_data = {
            "access_token": access_token,
            "params": {
                "from": from_date.isoformat(timespec='milliseconds'),
                "to": to_date.isoformat(timespec='milliseconds'),
                "productOrderStatuses": ["PAYED"],
                "placeOrderStatusType": "OK",
                "fulfillment": False,
                "pageSize": page_size,
                "page": page
            }
        }
        
        response = requests.post(
            "http://localhost:8001/api/orders/payed",
            json=request_data
        )
        
        if response.status_code != 200:
            break
        
        data = response.json()
        orders = data['orders']
        
        if not orders:
            break
        
        all_orders.extend(orders)
        print(f"已获取 {len(all_orders)} 个订单...")
        
        # 如果返回数量少于每页数量，说明是最后一页
        if len(orders) < page_size:
            break
        
        page += 1
    
    return all_orders

# 使用示例
tz = pytz.timezone('Asia/Seoul')
from_date = datetime(2024, 2, 1, 0, 0, 0, tzinfo=tz)
to_date = datetime(2024, 2, 11, 23, 59, 59, tzinfo=tz)

orders = get_all_payed_orders(access_token, from_date, to_date)
print(f"总共获取 {len(orders)} 个订单")
```

### 示例 3: 查询多种状态的订单

```python
request_data = {
    "access_token": access_token,
    "params": {
        "from": "2024-02-10T00:00:00.000+09:00",
        "to": "2024-02-11T23:59:59.999+09:00",
        "productOrderStatuses": ["PAYED", "DELIVERING", "DELIVERED"],
        "placeOrderStatusType": "OK",
        "fulfillment": False,
        "pageSize": 100,
        "page": 1
    }
}

response = requests.post(
    "http://localhost:8001/api/orders/payed",
    json=request_data
)
```

## 使用辅助工具

为了简化参数构建，可以使用 `params_builder.py` 工具：

```python
from params_builder import build_payed_orders_params
import requests

# 获取 token
token_response = requests.post("http://localhost:8001/api/token")
access_token = token_response.json()['access_token']

# 使用辅助工具构建参数（查询最近 3 天）
params = build_payed_orders_params(days=3, page_size=50)

# 发送请求
request_data = {
    "access_token": access_token,
    "params": params
}

response = requests.post(
    "http://localhost:8001/api/orders/payed",
    json=request_data
)
```

## 常见错误

### 1. 日期格式错误

**错误示例:**
```json
{
  "from": "2024-02-11",  // ❌ 缺少时间和时区
  "to": "2024-02-12"
}
```

**正确示例:**
```json
{
  "from": "2024-02-11T00:00:00.000+09:00",  // ✅ 完整格式
  "to": "2024-02-12T23:59:59.999+09:00"
}
```

### 2. 时区错误

**常见问题:**
- 使用 UTC 时间而不是韩国时间
- 忘记添加时区信息

**解决方案:**
始终使用韩国时区 (Asia/Seoul, UTC+9)

### 3. 参数类型错误

**错误示例:**
```json
{
  "productOrderStatuses": "PAYED",  // ❌ 应该是数组
  "pageSize": "100",  // ❌ 应该是数字
  "fulfillment": "false"  // ❌ 应该是布尔值
}
```

**正确示例:**
```json
{
  "productOrderStatuses": ["PAYED"],  // ✅ 数组
  "pageSize": 100,  // ✅ 数字
  "fulfillment": false  // ✅ 布尔值
}
```

## 响应数据结构

```json
{
  "success": true,
  "orders": [
    {
      "productOrderId": "2024021100001",
      "productOrderStatus": "PAYED",
      "orderDate": "2024-02-11T10:30:00+09:00",
      "ordererId": "userId123",
      "ordererName": "买家姓名",
      "productName": "商品名称",
      "quantity": 2,
      "totalPaymentAmount": 50000,
      ...
    }
  ],
  "total_count": 5,
  "message": "成功获取 5 条订单"
}
```

## 更多信息

- [API 完整文档](http://localhost:8001/docs)
- [错误代码说明](../API_GUIDE.md)
- [物流公司代码](../DELIVERY_CODES.md)
