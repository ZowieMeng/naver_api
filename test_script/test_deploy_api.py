#!/usr/bin/env python
"""
Naver Commerce Deploy API 测试脚本
测试所有 API 端点功能
"""

import requests
import json
from datetime import datetime

# API 基础 URL
BASE_URL = "http://localhost:8001"


def print_section(title):
    """打印分隔标题"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_response(response):
    """打印响应内容"""
    print(f"状态码: {response.status_code}")
    try:
        print(f"响应内容:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"响应内容: {response.text}")


def test_health_check():
    """测试健康检查"""
    print_section("测试 1: 健康检查")
    
    # 测试根路径
    print("\n1.1 测试根路径 GET /")
    response = requests.get(f"{BASE_URL}/")
    print_response(response)
    
    # 测试健康检查端点
    print("\n1.2 测试健康检查 GET /health")
    response = requests.get(f"{BASE_URL}/health")
    print_response(response)


def test_get_token():
    """测试获取访问令牌"""
    print_section("测试 2: 获取访问令牌")
    
    print("\n2.1 使用默认配置获取 Token")
    response = requests.post(f"{BASE_URL}/api/token")
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('access_token')
        print(f"\n✓ Token 获取成功: {token[:50]}...")
        return token
    else:
        print("\n✗ Token 获取失败")
        return None


def test_get_payed_orders(access_token):
    """测试获取已付款订单"""
    print_section("测试 3: 获取已付款订单")
    
    if not access_token:
        print("⚠️  跳过测试: 需要有效的 access_token")
        return []
    
    print("\n3.1 获取最近 1 天的已付款订单")
    
    # 计算日期范围
    from datetime import datetime, timedelta
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
    
    response = requests.post(f"{BASE_URL}/api/orders/payed", json=request_data)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        orders = data.get('orders', [])
        print(f"\n✓ 获取到 {len(orders)} 个订单")
        return orders
    else:
        print("\n✗ 订单获取失败")
        return []


def test_dispatch_orders(access_token, order_sample=None):
    """测试上传发货状态"""
    print_section("测试 4: 上传订单发货状态")
    
    if not access_token:
        print("⚠️  跳过测试: 需要有效的 access_token")
        return
    
    # 使用示例数据或真实订单
    if order_sample:
        print("\n4.1 使用真实订单数据测试")
        product_order_id = order_sample.get('productOrderId')
    else:
        print("\n4.1 使用示例数据测试")
        product_order_id = "TEST_ORDER_12345"
    
    dispatch_data = {
        "product_orders": [
            {
                "productOrderId": product_order_id,
                "deliveryMethod": "DELIVERY",
                "deliveryCompanyCode": "CJGLS",
                "trackingNumber": "1234567890123",
                "dispatchDate": datetime.now().isoformat()
            }
        ],
        "access_token": access_token
    }
    
    print(f"\n请求数据:")
    print(json.dumps(dispatch_data, indent=2, ensure_ascii=False))
    
    response = requests.post(
        f"{BASE_URL}/api/orders/dispatch",
        json=dispatch_data
    )
    print_response(response)
    
    if response.status_code == 200:
        print("\n✓ 发货状态上传成功")
    else:
        print("\n✗ 发货状态上传失败")


def main():
    """主测试函数"""
    print("\n" + "=" * 80)
    print("  Naver Commerce Deploy API - 完整测试")
    print("=" * 80)
    print(f"  测试服务器: {BASE_URL}")
    print(f"  测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # 检查服务是否运行
    try:
        requests.get(f"{BASE_URL}/health", timeout=2)
    except:
        print("\n❌ 错误: 无法连接到服务器")
        print("请先启动服务: python deploy_api.py")
        print("或运行启动脚本: ./start_deploy_api.sh")
        return
    
    # 执行测试
    test_health_check()
    
    access_token = test_get_token()
    
    orders = test_get_payed_orders(access_token)
    
    # 如果有真实订单，使用第一个订单测试发货
    if orders and len(orders) > 0:
        test_dispatch_orders(access_token, orders[0])
    else:
        test_dispatch_orders(access_token)
    
    # 测试总结
    print_section("测试完成")
    print("\n所有测试已完成!")
    print("\n提示:")
    print("  - 查看详细 API 文档: http://localhost:8001/docs")
    print("  - 查看 ReDoc 文档: http://localhost:8001/redoc")


if __name__ == "__main__":
    main()
