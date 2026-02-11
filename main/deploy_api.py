#!/usr/bin/env python
"""
Naver Commerce API - Deploy Service
FastAPI 部署服务接口
提供订单查询和发货状态上传功能
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import uvicorn
from datetime import datetime
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入业务逻辑函数
from main.setp_function_code import (
    get_access_token,
    get_payed_orders,
    dispatch_product_orders
)

# ==================== Pydantic 数据模型 ====================

class TokenResponse(BaseModel):
    """Token 响应模型"""
    success: bool
    access_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: Optional[str] = None
    error: Optional[str] = None


class DispatchOrderItem(BaseModel):
    """发货订单项模型"""
    productOrderId: str = Field(..., description="产品订单ID")
    deliveryMethod: str = Field(default="DELIVERY", description="配送方式")
    deliveryCompanyCode: str = Field(..., description="物流公司代码")
    trackingNumber: str = Field(..., description="运单号")
    dispatchDate: Optional[str] = Field(None, description="发货日期 (ISO 8601格式)")


class DispatchRequest(BaseModel):
    """发货请求模型"""
    product_orders: List[DispatchOrderItem] = Field(..., description="发货订单列表")
    access_token: Optional[str] = Field(None, description="访问令牌（可选，不提供则自动获取）")


class OrdersQueryRequest(BaseModel):
    """订单查询请求模型"""
    access_token: str = Field(..., description="访问令牌")
    params: dict = Field(..., description="查询参数字典")


# ==================== FastAPI 应用 ====================

app = FastAPI(
    title="Naver Commerce Deploy API",
    description="Naver 商城部署服务 - 订单查询与发货管理",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# ==================== API 端点 ====================

@app.get("/", tags=["Health"])
async def root():
    """
    服务根路径 - 健康检查
    """
    return {
        "service": "Naver Commerce Deploy API",
        "version": "2.0.0",
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "get_token": "POST /api/token",
            "get_payed_orders": "POST /api/orders/payed",
            "dispatch_orders": "POST /api/orders/dispatch"
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    健康检查端点
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/token", response_model=TokenResponse, tags=["Authentication"])
async def get_token_endpoint(
    client_id: Optional[str] = Query(None, description="客户端ID"),
    client_secret: Optional[str] = Query(None, description="客户端密钥")
):
    """
    获取 Naver Commerce API 访问令牌
    
    **功能说明:**
    - 生成 clientSecret token
    - 获取有效的 access_token
    - 返回令牌和过期时间
    
    **参数:**
    - client_id: 客户端 ID (可选，不提供则使用默认配置)
    - client_secret: 客户端密钥 (可选，不提供则使用默认配置)
    
    **返回:**
    - success: 是否成功
    - access_token: 访问令牌
    - expires_in: 过期时间（秒）
    - token_type: 令牌类型
    - error: 错误信息（如果失败）
    """
    try:
        result = get_access_token(
            client_id=client_id,
            client_secret=client_secret
        )
        
        if result['success']:
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "access_token": result['access_token'],
                    "expires_in": result['expires_in'],
                    "token_type": result['token_type'],
                    "message": "Token 获取成功"
                }
            )
        else:
            raise HTTPException(
                status_code=500,
                detail={
                    "success": False,
                    "error": result['error'],
                    "message": "Token 获取失败"
                }
            )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": str(e),
                "message": "服务器内部错误"
            }
        )


@app.post("/api/orders/payed", tags=["Orders"])
async def get_payed_orders_endpoint(request: OrdersQueryRequest):
    """
    获取已付款订单列表
    
    **功能说明:**
    - 查询指定参数的已付款订单
    - 订单状态为 PAYED
    - 返回订单详细信息列表
    
    **请求参数:**
    ```json
    {
        "access_token": "访问令牌",
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
    
    **返回:**
    - success: 是否成功
    - orders: 订单列表
    - total_count: 订单总数
    - error: 错误信息（如果失败）
    """
    try:
        result = get_payed_orders(
            access_token=request.access_token,
            params=request.params
        )
        
        if result['success']:
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "orders": result['orders'],
                    "total_count": result['total_count'],
                    "message": f"成功获取 {result['total_count']} 条订单"
                }
            )
        else:
            raise HTTPException(
                status_code=500,
                detail={
                    "success": False,
                    "error": result['error'],
                    "message": "订单获取失败"
                }
            )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": str(e),
                "message": "服务器内部错误"
            }
        )


@app.post("/api/orders/dispatch", tags=["Orders"])
async def dispatch_orders_endpoint(request: DispatchRequest):
    """
    上传订单发货状态
    
    **功能说明:**
    - 批量上传订单的发货信息
    - 包含物流公司、运单号、发货时间等信息
    - 更新订单状态到 Naver Commerce
    
    **请求参数:**
    ```json
    {
        "product_orders": [
            {
                "productOrderId": "订单ID",
                "deliveryMethod": "DELIVERY",
                "deliveryCompanyCode": "物流公司代码",
                "trackingNumber": "运单号",
                "dispatchDate": "2026-02-11T10:00:00+09:00"
            },
            {
                "productOrderId": "订单ID2",
                "deliveryMethod": "DELIVERY",
                "deliveryCompanyCode": "物流公司代码2",
                "trackingNumber": "运单号2",
                "dispatchDate": "2026-02-11T10:00:00+09:00"
            }
        ],
        "access_token": "访问令牌（可选）"
    }
    ```
    
    **返回:**
    - success: 是否成功
    - response: API 响应数据
    - error: 错误信息（如果失败）
    """
    try:
        # 转换 Pydantic 模型为字典
        product_orders = [order.dict() for order in request.product_orders]
        
        # 如果没有提供 dispatchDate，自动添加当前时间
        for order in product_orders:
            if not order.get('dispatchDate'):
                order['dispatchDate'] = datetime.now().isoformat()
        
        # 调用业务逻辑函数
        result = dispatch_product_orders(
            product_orders=product_orders,
            access_token=request.access_token
        )
        
        if result['success']:
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "response": result['response'],
                    "message": "订单发货状态上传成功"
                }
            )
        else:
            raise HTTPException(
                status_code=500,
                detail={
                    "success": False,
                    "error": result['error'],
                    "message": "订单发货状态上传失败"
                }
            )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": str(e),
                "message": "服务器内部错误"
            }
        )


# ==================== 启动服务 ====================

if __name__ == "__main__":
    print("=" * 100)
    print("🚀 启动 Naver Commerce Deploy API 服务")
    print("=" * 100)
    print(f"📍 服务地址: http://0.0.0.0:8001")
    print(f"📖 API 文档: http://localhost:8001/docs")
    print(f"📘 ReDoc 文档: http://localhost:8001/redoc")
    print("=" * 100)
    print("🔌 可用接口:")
    print("  ├─ POST /api/token              - 获取访问令牌")
    print("  ├─ POST /api/orders/payed       - 获取已付款订单")
    print("  ├─ POST /api/orders/dispatch    - 上传发货状态")
    print("  ├─ GET  /                       - 服务状态")
    print("  └─ GET  /health                 - 健康检查")
    print("=" * 100)
    
    uvicorn.run(
        "deploy_api:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
