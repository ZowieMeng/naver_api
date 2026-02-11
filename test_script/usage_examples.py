#!/usr/bin/env python
"""
FastAPI 服务使用示例
演示如何调用 Naver Commerce Deploy API 的各个端点
"""

import requests
import json
from datetime import datetime


# ==================== 配置 ====================
API_BASE_URL = "http://localhost:8001"


# ==================== 示例 1: 获取访问令牌 ====================
def example_get_token():
    """示例：获取访问令牌"""
    print("\n" + "=" * 80)
    print("示例 1: 获取访问令牌")
    print("=" * 80)
    
    url = f"{API_BASE_URL}/api/token"
    
    print(f"\n请求 URL: {url}")
    print("请求方法: POST")
    
    response = requests.post(url)
    
    print(f"\n响应状态码: {response.status_code}")
    print("响应内容:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    
    if response.status_code == 200:
        data = response.json()
        return data.get('access_token')
    return None


# ==================== 示例 2: 获取已付款订单 ====================
def example_get_payed_orders(access_token):
    """示例：获取已付款订单"""
    print("\n" + "=" * 80)
    print("示例 2: 获取已付款订单")
    print("=" * 80)
    
    if not access_token:
        print("❌ 需要有效的 access_token")
        return []
    
    from datetime import timedelta
    import pytz
    
    url = f"{API_BASE_URL}/api/orders/payed"
    
    # 计算日期范围
    tz = pytz.timezone('Asia/Seoul')
    now = datetime.now(tz)
    from_date = now - timedelta(days=1)
    
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
    
    print(f"\n请求 URL: {url}")
    print("请求方法: POST")
    print("请求体:")
    print(json.dumps(request_data, indent=2, ensure_ascii=False))
    
    response = requests.post(url, json=request_data)
    
    print(f"\n响应状态码: {response.status_code}")
    print("响应内容:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    
    if response.status_code == 200:
        data = response.json()
        return data.get('orders', [])
    return []


# ==================== 示例 3: 上传发货状态 ====================
def example_dispatch_orders(access_token):
    """示例：上传发货状态"""
    print("\n" + "=" * 80)
    print("示例 3: 上传发货状态")
    print("=" * 80)
    
    if not access_token:
        print("❌ 需要有效的 access_token")
        return
    
    url = f"{API_BASE_URL}/api/orders/dispatch"
    
    # 准备发货数据
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
    
    print(f"\n请求 URL: {url}")
    print("请求方法: POST")
    print("请求体:")
    print(json.dumps(dispatch_data, indent=2, ensure_ascii=False))
    
    response = requests.post(url, json=dispatch_data)
    
    print(f"\n响应状态码: {response.status_code}")
    print("响应内容:")
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print(response.text)


# ==================== 示例 4: 批量上传多个订单 ====================
def example_batch_dispatch(access_token, orders):
    """示例：批量上传多个订单的发货状态"""
    print("\n" + "=" * 80)
    print("示例 4: 批量上传多个订单")
    print("=" * 80)
    
    if not access_token:
        print("❌ 需要有效的 access_token")
        return
    
    if not orders:
        print("⚠️  没有订单数据，跳过批量上传示例")
        return
    
    url = f"{API_BASE_URL}/api/orders/dispatch"
    
    # 从真实订单构建发货数据（仅作示例，不会真正上传）
    product_orders = []
    for idx, order in enumerate(orders[:3]):  # 只处理前 3 个订单
        product_orders.append({
            "productOrderId": order.get('productOrderId'),
            "deliveryMethod": "DELIVERY",
            "deliveryCompanyCode": "CJGLS",
            "trackingNumber": f"TEST{idx:010d}",  # 测试运单号
            "dispatchDate": datetime.now().isoformat()
        })
    
    dispatch_data = {
        "product_orders": product_orders,
        "access_token": access_token
    }
    
    print(f"\n请求 URL: {url}")
    print("请求方法: POST")
    print(f"批量上传 {len(product_orders)} 个订单")
    print("\n请求体:")
    print(json.dumps(dispatch_data, indent=2, ensure_ascii=False))
    
    print("\n⚠️  这是一个演示示例，不会真正调用 API")
    print("如需真正上传，请取消下面的注释：")
    print("# response = requests.post(url, json=dispatch_data)")


# ==================== 示例 5: 完整工作流 ====================
def example_complete_workflow():
    """示例：完整工作流 - 从获取订单到上传发货"""
    print("\n" + "=" * 80)
    print("示例 5: 完整工作流")
    print("=" * 80)
    
    print("\n步骤 1: 获取访问令牌")
    token_response = requests.post(f"{API_BASE_URL}/api/token")
    if token_response.status_code != 200:
        print("❌ Token 获取失败")
        return
    
    access_token = token_response.json().get('access_token')
    print(f"✓ Token 获取成功: {access_token[:50]}...")
    
    print("\n步骤 2: 查询已付款订单")
    
    from datetime import timedelta
    import pytz
    
    tz = pytz.timezone('Asia/Seoul')
    now = datetime.now(tz)
    from_date = now - timedelta(days=1)
    
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
        f"{API_BASE_URL}/api/orders/payed",
        json=request_data
    )
    
    if orders_response.status_code != 200:
        print("❌ 订单查询失败")
        return
    
    orders = orders_response.json().get('orders', [])
    print(f"✓ 获取到 {len(orders)} 个订单")
    
    if not orders:
        print("⚠️  没有待发货的订单")
        return
    
    print("\n步骤 3: 准备发货数据")
    # 这里应该从你的物流系统获取实际的运单号
    # 示例中使用模拟数据
    product_orders = []
    for order in orders[:5]:  # 只处理前 5 个订单
        product_orders.append({
            "productOrderId": order.get('productOrderId'),
            "deliveryMethod": "DELIVERY",
            "deliveryCompanyCode": "CJGLS",
            "trackingNumber": "模拟运单号",  # 实际应该是真实运单号
        })
    
    print(f"准备上传 {len(product_orders)} 个订单的发货信息")
    
    print("\n步骤 4: 上传发货状态")
    print("⚠️  这是演示，不会真正上传")
    print("实际使用时，请确保运单号是真实有效的")
    
    # 实际上传代码（已注释）：
    # dispatch_data = {
    #     "product_orders": product_orders,
    #     "access_token": access_token
    # }
    # response = requests.post(
    #     f"{API_BASE_URL}/api/orders/dispatch",
    #     json=dispatch_data
    # )
    # if response.status_code == 200:
    #     print("✓ 发货状态上传成功")


# ==================== 主函数 ====================
def main():
    """运行所有示例"""
    print("=" * 80)
    print("  Naver Commerce Deploy API - 使用示例")
    print("=" * 80)
    print(f"  API 服务: {API_BASE_URL}")
    print(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # 检查服务是否运行
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=2)
        if response.status_code != 200:
            raise Exception("服务不健康")
    except Exception as e:
        print("\n❌ 无法连接到 API 服务")
        print("请先启动服务：")
        print("  python deploy_api.py")
        print("  或")
        print("  ./start_deploy_api.sh")
        return
    
    print("\n✓ API 服务运行正常")
    
    # 运行示例
    access_token = example_get_token()
    orders = example_get_payed_orders(access_token)
    example_dispatch_orders(access_token)
    example_batch_dispatch(access_token, orders)
    example_complete_workflow()
    
    # 总结
    print("\n" + "=" * 80)
    print("所有示例运行完成！")
    print("=" * 80)
    print("\n更多信息：")
    print("  - API 文档: http://localhost:8001/docs")
    print("  - ReDoc 文档: http://localhost:8001/redoc")
    print("  - 详细说明: README.md")


if __name__ == "__main__":
    main()
