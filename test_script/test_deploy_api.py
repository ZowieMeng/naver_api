#!/usr/bin/env python
"""
Naver Commerce Deploy API 测试脚本
测试所有 API 端点功能
"""

import requests
import json
from datetime import datetime

# API 基础 URL
BASE_URL = "https://werewolf-deep-gnu.ngrok-free.app"


def print_section(title):
    """打印分隔标题"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_response(response):
    """打印响应内容"""
    print(f"状态码: {response.status_code}")
    try:
        print(
            f"响应内容:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
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


def test_get_payed_orders():
    """测试获取已付款订单 - 分24小时时间段循环查询"""
    print_section("测试 3: 获取已付款订单（分时间段查询）")

    from datetime import datetime, timedelta
    import pytz

    tz = pytz.timezone('Asia/Seoul')
    now = datetime.now(tz)

    # 设置开始时间为今天00:00:00
    current_end = now

    all_orders = []
    page_size = 300
    total_count = 0
    time_slot_index = 0
    empty_slot_count = 0  # 连续空时间段计数
    max_empty_slots = 1  # 连续空时间段阈值

    print(f"\n开始循环查询，每个时间段24小时，pageSize={page_size}")
    print(f"停止条件：第一个时间段无数据 或 连续{max_empty_slots}个时间段无数据")
    print("=" * 80)

    while True:
        time_slot_index += 1
        # 计算当前24小时时间段
        current_start = current_end - timedelta(hours=24)

        print(f"\n【时间段 {time_slot_index}】")
        print(f"查询范围: {current_start.isoformat()} ~ {current_end.isoformat()}")

        # 当前时间段的订单
        slot_orders = []
        page = 1
        is_first_request = True

        # 对当前时间段进行分页查询
        while True:
            print(f"  → 请求第 {page} 页...", end=" ")

            request_data = {
                "params": {
                    "from": current_start.isoformat(timespec='milliseconds'),
                    "to": current_end.isoformat(timespec='milliseconds'),
                    "productOrderStatuses": ["PAYED"],
                    "placeOrderStatusType": "OK",
                    "pageSize": page_size,
                    "page": page
                }
            }

            try:
                response = requests.post(
                    f"{BASE_URL}/api/orders/payed", json=request_data)

                if response.status_code == 200:
                    data = response.json()
                    orders = data.get('orders', [])
                    order_count = len(orders)

                    print(f"获取 {order_count} 个订单")

                    # 如果是第一次请求且返回0，停止整个循环
                    if is_first_request and order_count == 0:
                        if time_slot_index == 1:
                            print(f"  ✓ 第一个时间段无数据，停止查询")
                            break
                        else:
                            print(f"  ✓ 当前时间段无数据，进入下一时间段")
                            break

                    is_first_request = False

                    # 添加到当前时间段订单列表
                    slot_orders.extend(orders)

                    # 如果返回数量小于pageSize，说明这个时间段已查完
                    if order_count < page_size:
                        print(f"  ✓ 当前时间段查询完成")
                        break

                    # 继续下一页
                    page += 1
                else:
                    print(f"✗ 请求失败 (状态码: {response.status_code})")
                    break

            except Exception as e:
                print(f"✗ 请求异常: {str(e)}")
                break

        # 如果第一个时间段第一次请求就是0，停止整个循环
        if time_slot_index == 1 and len(slot_orders) == 0:
            print(f"\n首个时间段无数据，停止查询")
            break

        # 统计当前时间段
        slot_count = len(slot_orders)
        all_orders.extend(slot_orders)
        total_count += slot_count

        print(f"  ✓ 时间段 {time_slot_index} 共获取: {slot_count} 个订单")
        print(f"  累计获取: {total_count} 个订单")

        # 判断是否继续查询
        if slot_count == 0:
            empty_slot_count += 1
            print(f"  ⚠️  连续空时间段: {empty_slot_count}/{max_empty_slots}")
            
            # 连续空时间段达到阈值，停止查询
            if empty_slot_count >= max_empty_slots:
                print(f"\n连续{max_empty_slots}个时间段无数据，停止查询")
                break
        else:
            # 有数据则重置连续空时间段计数
            empty_slot_count = 0

        # 移动到上一个24小时时间段
        current_end = current_start

    # 输出统计信息
    print("\n" + "=" * 80)
    print(f"【查询完成】")
    print(f"  总时间段数: {time_slot_index}")
    print(f"  总订单数: {total_count}")
    print("=" * 80)

    # 保存所有订单到JSON文件
    if all_orders:
        output_file = "./sample_orders.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_orders, f, indent=2, ensure_ascii=False)
        print(f"\n✓ 订单数据已保存到: {output_file}")
    else:
        print(f"\n⚠️  未获取到任何订单")

    return all_orders


def test_dispatch_orders(order_sample=None):
    """测试上传发货状态"""
    print_section("测试 4: 上传订单发货状态")

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
        ]
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
        requests.get(f"{BASE_URL}/health", timeout=10)
    except:
        print("\n❌ 错误: 无法连接到服务器")
        print("请先启动服务: python deploy_api.py")
        print("或运行启动脚本: ./start_deploy_api.sh")
        return

    # 执行测试
    # test_health_check()

    orders = test_get_payed_orders()

    # # 如果有真实订单，使用第一个订单测试发货
    # if orders and len(orders) > 0:
    #     test_dispatch_orders(orders[0])
    # else:
    #     test_dispatch_orders()

    # 测试总结
    print_section("测试完成")
    print("\n所有测试已完成!")
    print("\n提示:")
    print("  - 查看详细 API 文档: http://localhost:8001/docs")
    print("  - 查看 ReDoc 文档: http://localhost:8001/redoc")


if __name__ == "__main__":
    main()
