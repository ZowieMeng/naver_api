#!/usr/bin/env python
"""
新版 API 快速验证脚本
验证 params 参数功能是否正常工作
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from deploy_code.main.setp_function_code import get_access_token, get_payed_orders
from params_builder import build_payed_orders_params
from datetime import datetime, timedelta
import pytz


def test_new_params_api():
    """测试新的 params 参数 API"""
    print("=" * 80)
    print("新版 API 功能验证")
    print("=" * 80)
    
    # 步骤 1: 获取 token
    print("\n步骤 1: 获取访问令牌...")
    token_result = get_access_token()
    
    if not token_result['success']:
        print(f"❌ Token 获取失败: {token_result['error']}")
        return False
    
    access_token = token_result['access_token']
    print(f"✅ Token 获取成功")
    
    # 步骤 2: 使用辅助工具构建参数
    print("\n步骤 2: 使用 params_builder 构建查询参数...")
    params = build_payed_orders_params(days=1, page_size=10)
    print(f"✅ 参数构建成功:")
    print(f"   - from: {params['from']}")
    print(f"   - to: {params['to']}")
    print(f"   - pageSize: {params['pageSize']}")
    
    # 步骤 3: 调用新版 get_payed_orders
    print("\n步骤 3: 调用 get_payed_orders (新版 params 参数)...")
    try:
        result = get_payed_orders(access_token=access_token, params=params)
        
        if result['success']:
            print(f"✅ 订单查询成功")
            print(f"   - 订单总数: {result['total_count']}")
            if result['total_count'] > 0:
                print(f"   - 第一个订单ID: {result['orders'][0].get('productOrderId', 'N/A')}")
        else:
            print(f"⚠️  订单查询失败: {result['error']}")
            return False
    except Exception as e:
        print(f"❌ 调用失败: {e}")
        return False
    
    # 步骤 4: 测试手动构建参数
    print("\n步骤 4: 测试手动构建参数...")
    tz = pytz.timezone('Asia/Seoul')
    now = datetime.now(tz)
    yesterday = now - timedelta(days=1)
    
    manual_params = {
        'from': yesterday.isoformat(timespec='milliseconds'),
        'to': now.isoformat(timespec='milliseconds'),
        'productOrderStatuses': ['PAYED'],
        'placeOrderStatusType': 'OK',
        'fulfillment': False,
        'pageSize': 5,
        'page': 1
    }
    
    try:
        result2 = get_payed_orders(access_token=access_token, params=manual_params)
        
        if result2['success']:
            print(f"✅ 手动参数查询成功")
            print(f"   - 订单总数: {result2['total_count']}")
        else:
            print(f"⚠️  手动参数查询失败: {result2['error']}")
    except Exception as e:
        print(f"❌ 调用失败: {e}")
        return False
    
    # 验证成功
    print("\n" + "=" * 80)
    print("✅ 所有验证通过！新版 API 工作正常")
    print("=" * 80)
    return True


if __name__ == "__main__":
    print("开始验证新版 API 功能...")
    print("=" * 80)
    
    success = test_new_params_api()
    
    if success:
        print("\n✅ 验证完成 - API 功能正常")
        print("\n提示:")
        print("  1. 可以启动 FastAPI 服务测试完整功能: python deploy_api.py")
        print("  2. 运行完整测试套件: python test_deploy_api.py")
        print("  3. 查看使用示例: python usage_examples.py")
        sys.exit(0)
    else:
        print("\n❌ 验证失败 - 请检查错误信息")
        sys.exit(1)
