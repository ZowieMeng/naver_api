#!/usr/bin/env python
import time
import bcrypt
import pybase64
import requests
import datetime
import json
import pytz

# ==================== 配置信息 ====================
clientId = "3Nu2hAaKhBp1Aj6jo1goP3"
clientSecret = "$2a$04$/HKy4NTQW/nFKpvN5b/Suu"


##=============================================================================================================
# 第一步: 构建 clientSecret token
def build_client_secret_token(client_id=None, client_secret=None):
    """
    构建 Naver API 的 clientSecret token
    
    Args:
        client_id: 客户端 ID (默认使用全局配置)
        client_secret: 客户端密钥 (默认使用全局配置)
    
    Returns:
        tuple: (clientSecretToken, timestamp)
    """
    if client_id is None:
        client_id = clientId
    if client_secret is None:
        client_secret = clientSecret
    
    timestamp = round(time.time() * 1000)
    
    # 밑줄로 연결하여 password 생성
    password = client_id + "_" + str(timestamp)
    
    # bcrypt 해싱
    hashed = bcrypt.hashpw(password.encode('utf-8'), client_secret.encode('utf-8'))
    
    # base64 인코딩
    token = pybase64.standard_b64encode(hashed).decode('utf-8')
    
    print(f"✓ ClientSecret Token 生成成功")
    print(f"  Timestamp: {timestamp}")
    
    return token, timestamp


##=============================================================================================================
# 第二步: 获取 access_token

def get_access_token(client_id=None, client_secret=None):
    """
    获取 Naver Commerce API 的 access token
    
    Args:
        client_id: 客户端 ID (默认使用全局配置)
        client_secret: 客户端密钥 (默认使用全局配置)
    
    Returns:
        dict: 包含 token 信息
            - success: bool
            - access_token: str
            - expires_in: int
            - token_type: str
            - error: str
    """
    if client_id is None:
        client_id = clientId
    if client_secret is None:
        client_secret = clientSecret
    
    # 构建 token
    client_secret_token, timestamp = build_client_secret_token(client_id, client_secret)
    
    url = "https://api.commerce.naver.com/external/v1/oauth2/token"
    
    payload = {
        'grant_type': 'client_credentials',
        'timestamp': int(timestamp),
        'client_id': client_id,
        'client_secret_sign': client_secret_token,
        'scope': 'category.read',
        'type': 'SELF',
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.post(url, headers=headers, data=payload)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Access Token 获取成功")
            print(f"  Token: {data.get('access_token', '')[:50]}...")
            print(f"  Expires in: {data.get('expires_in')} seconds")
            
            return {
                'success': True,
                'access_token': data.get('access_token'),
                'expires_in': data.get('expires_in'),
                'token_type': data.get('token_type'),
                'error': None
            }
        else:
            print(f"✗ Access Token 获取失败: HTTP {response.status_code}")
            return {
                'success': False,
                'access_token': None,
                'error': f"HTTP {response.status_code}: {response.text}"
            }
    except Exception as e:
        print(f"✗ 异常: {e}")
        return {
            'success': False,
            'access_token': None,
            'error': str(e)
        }
##=============================================================================================================
# 涉及业务方法: 获取已付款订单

def get_payed_orders(access_token, params):
    """
    获取已付款订单
    
    Args:
        access_token: API access token
        params: 查询参数字典，例如:
            {
                'from': '2024-02-10T00:00:00.000+09:00',
                'to': '2024-02-11T23:59:59.999+09:00',
                'productOrderStatuses': ['PAYED'],
                'placeOrderStatusType': 'OK',
                'fulfillment': False,
                'pageSize': 100,
                'page': 1
            }
    
    Returns:
        dict: 包含订单信息
            - success: bool
            - orders: list, 订单列表
            - total_count: int, 订单总数
            - error: str
    """
    url = "https://api.commerce.naver.com/external/v1/pay-order/seller/product-orders"
    
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    tz = pytz.timezone('Asia/Seoul')
    now = datetime.datetime.now(tz)#-datetime.timedelta(days=days)
    from_date = now - datetime.timedelta(days=1)
    to_date = now
    
    # 格式化日期
    from_date_str = from_date.isoformat(timespec='milliseconds')
    to_date_str = to_date.isoformat(timespec='milliseconds')
    payload = {
        'from': from_date_str,
        'to': to_date_str,
    }
    payload.update(params)
    
    try:
        response = requests.get(url, headers=headers, params=payload)
        
        if response.status_code == 200:
            data = response.json()
            print(f' req raw json data : {data}')
            orders = data.get('data', {}).get('contents', [])
            
            print(f"✓ 订单获取成功")
            print(f"  订单总数: {len(orders)}")
            
            return {
                'success': True,
                'orders': orders,
                'total_count': len(orders),
                'error': None
            }
        else:
            print(f"✗ 订单获取失败: HTTP {response.status_code}")
            print(f'rsp text:{response.text}')
            return {
                'success': False,
                'orders': [],
                'total_count': 0,
                'error': f"HTTP {response.status_code}: {response.text}"
            }
    except Exception as e:
        print(f"✗ 异常: {e}")
        return {
            'success': False,
            'orders': [],
            'total_count': 0,
            'error': str(e)
        }
    


##=============================================================================================================
# 涉及业务方法: 上传订单发货状态到 Naver Commerce API

def dispatch_product_orders(product_orders, access_token=None, client_id=None, client_secret=None):
    """
    上传订单发货状态到 Naver Commerce API
    
    Args:
        product_orders: 产品订单列表,格式:
            [
                {
                    "productOrderId": "订单ID",
                    "deliveryMethod": "DELIVERY",  # 配送方式
                    "deliveryCompanyCode": "物流公司代码",
                    "trackingNumber": "运单号",
                    "dispatchDate": "发货日期 (ISO 8601格式)"
                }
            ]
        access_token: 访问令牌 (如果未提供,将自动获取)
        client_id: 客户端 ID (默认使用全局配置)
        client_secret: 客户端密钥 (默认使用全局配置)
    
    Returns:
        dict: 包含处理结果
            - success: bool
            - response: dict (API 响应数据)
            - error: str
    """
    # 如果没有提供 access_token,先获取
    if access_token is None:
        token_result = get_access_token(client_id, client_secret)
        if not token_result['success']:
            return {
                'success': False,
                'response': None,
                'error': f"获取 access_token 失败: {token_result['error']}"
            }
        access_token = token_result['access_token']
    
    url = "https://api.commerce.naver.com/external/v1/pay-order/seller/product-orders/dispatch"
    
    payload = {
        "dispatchProductOrders": product_orders
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ 订单发货状态上传成功")
            print(f"  响应数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
            
            return {
                'success': True,
                'response': data,
                'error': None
            }
        else:
            error_msg = f"HTTP {response.status_code}: {response.text}"
            print(f"✗ 订单发货状态上传失败: {error_msg}")
            
            return {
                'success': False,
                'response': None,
                'error': error_msg
            }
    except Exception as e:
        print(f"✗ 异常: {e}")
        return {
            'success': False,
            'response': None,
            'error': str(e)
        }


if __name__ == "__main__":
    # 示例: 获取 access token
    token_info = get_access_token()
    
    if token_info['success']:
        access_token = token_info['access_token']
        
        # 示例: 获取已付款订单
        example_params = {
            'from': (datetime.datetime.now(pytz.timezone('Asia/Seoul')) - datetime.timedelta(days=2)).isoformat(timespec='milliseconds'),
            'to': datetime.datetime.now(pytz.timezone('Asia/Seoul')).isoformat(timespec='milliseconds'),
            'productOrderStatuses': ['PAYED'],
            'placeOrderStatusType': 'OK',
            'fulfillment': False,
            'pageSize': 100,
            'page': 1
        }
        orders_result = get_payed_orders(access_token, params=example_params)
        
        if orders_result['success']:
            orders = orders_result['orders']
            print(f"获取到 {len(orders)} 个已付款订单")
            
            # 示例: 上传订单发货状态 (假设我们有一个订单需要更新)
            if orders:
                sample_order = orders[0]  # 取第一个订单作为示例
                product_orders = [
                    {
                        "productOrderId": sample_order.get('productOrderId'),
                        "deliveryMethod": "DELIVERY",
                        "deliveryCompanyCode": "CJGLS",
                        "trackingNumber": "1234567890",
                        "dispatchDate": datetime.datetime.now().isoformat()
                    }
                ]
                
                dispatch_result = dispatch_product_orders(product_orders, access_token)
                
                if dispatch_result['success']:
                    print("订单发货状态上传成功")
                else:
                    print(f"订单发货状态上传失败: {dispatch_result['error']}")
        else:
            print(f"获取已付款订单失败: {orders_result['error']}")
    else:
        print(f"获取 access token 失败: {token_info['error']}")