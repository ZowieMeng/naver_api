#!/usr/bin/env python
"""
订单查询参数构建辅助工具
提供便捷的参数构建函数
"""

from datetime import datetime, timedelta
import pytz


def build_payed_orders_params(
    days=1,
    page_size=100,
    page=1,
    from_date=None,
    to_date=None,
    timezone='Asia/Seoul'
):
    """
    构建查询已付款订单的参数字典
    
    Args:
        days: 查询最近几天的订单（如果 from_date 和 to_date 未指定）
        page_size: 每页数量（1-100）
        page: 页码（从 1 开始）
        from_date: 开始日期（datetime 对象），如果指定则忽略 days 参数
        to_date: 结束日期（datetime 对象），如果指定则忽略 days 参数
        timezone: 时区（默认韩国时区）
    
    Returns:
        dict: 查询参数字典
    """
    tz = pytz.timezone(timezone)
    
    # 如果没有指定具体日期，则根据 days 计算
    if from_date is None or to_date is None:
        to_date = datetime.now(tz)
        from_date = to_date - timedelta(days=days)
    else:
        # 确保日期带有时区信息
        if from_date.tzinfo is None:
            from_date = tz.localize(from_date)
        if to_date.tzinfo is None:
            to_date = tz.localize(to_date)
    
    # 格式化为 ISO 8601 格式
    from_date_str = from_date.isoformat(timespec='milliseconds')
    to_date_str = to_date.isoformat(timespec='milliseconds')
    
    return {
        'from': from_date_str,
        'to': to_date_str,
        'productOrderStatuses': ['PAYED'],
        'placeOrderStatusType': 'OK',
        'fulfillment': False,
        'pageSize': page_size,
        'page': page
    }


def build_custom_orders_params(
    from_date,
    to_date,
    statuses=['PAYED'],
    place_order_type='OK',
    fulfillment=False,
    page_size=100,
    page=1,
    timezone='Asia/Seoul'
):
    """
    构建自定义订单查询参数
    
    Args:
        from_date: 开始日期（datetime 对象或 ISO 字符串）
        to_date: 结束日期（datetime 对象或 ISO 字符串）
        statuses: 订单状态列表
        place_order_type: 订单类型
        fulfillment: 是否使用物流服务
        page_size: 每页数量
        page: 页码
        timezone: 时区
    
    Returns:
        dict: 查询参数字典
    """
    tz = pytz.timezone(timezone)
    
    # 处理日期格式
    if isinstance(from_date, datetime):
        if from_date.tzinfo is None:
            from_date = tz.localize(from_date)
        from_date_str = from_date.isoformat(timespec='milliseconds')
    else:
        from_date_str = from_date
    
    if isinstance(to_date, datetime):
        if to_date.tzinfo is None:
            to_date = tz.localize(to_date)
        to_date_str = to_date.isoformat(timespec='milliseconds')
    else:
        to_date_str = to_date
    
    return {
        'from': from_date_str,
        'to': to_date_str,
        'productOrderStatuses': statuses,
        'placeOrderStatusType': place_order_type,
        'fulfillment': fulfillment,
        'pageSize': page_size,
        'page': page
    }


# ==================== 使用示例 ====================

if __name__ == "__main__":
    print("=" * 80)
    print("订单查询参数构建工具 - 使用示例")
    print("=" * 80)
    
    # 示例 1: 查询最近 1 天的订单
    print("\n示例 1: 查询最近 1 天的订单")
    params1 = build_payed_orders_params(days=1)
    print(f"参数: {params1}")
    
    # 示例 2: 查询最近 7 天的订单，每页 50 条
    print("\n示例 2: 查询最近 7 天的订单，每页 50 条")
    params2 = build_payed_orders_params(days=7, page_size=50)
    print(f"参数: {params2}")
    
    # 示例 3: 指定具体日期范围
    print("\n示例 3: 指定具体日期范围")
    tz = pytz.timezone('Asia/Seoul')
    from_dt = datetime(2024, 2, 1, 0, 0, 0, tzinfo=tz)
    to_dt = datetime(2024, 2, 10, 23, 59, 59, tzinfo=tz)
    params3 = build_payed_orders_params(from_date=from_dt, to_date=to_dt)
    print(f"参数: {params3}")
    
    # 示例 4: 自定义查询（包含多种状态）
    print("\n示例 4: 自定义查询（包含多种订单状态）")
    from_dt = datetime.now(tz) - timedelta(days=3)
    to_dt = datetime.now(tz)
    params4 = build_custom_orders_params(
        from_date=from_dt,
        to_date=to_dt,
        statuses=['PAYED', 'DELIVERING'],
        page_size=200
    )
    print(f"参数: {params4}")
    
    print("\n" + "=" * 80)
    print("提示：将这些参数传递给 API 的 params 字段")
    print("=" * 80)
    
    # 完整调用示例
    print("\n完整 API 调用示例:")
    print("""
import requests
from params_builder import build_payed_orders_params

# 获取 token
token_response = requests.post("http://localhost:8001/api/token")
access_token = token_response.json()['access_token']

# 构建查询参数
params = build_payed_orders_params(days=1)

# 调用 API
request_data = {
    "access_token": access_token,
    "params": params
}

response = requests.post(
    "http://localhost:8001/api/orders/payed",
    json=request_data
)

orders = response.json()['orders']
print(f"获取到 {len(orders)} 个订单")
    """)
