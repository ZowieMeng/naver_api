#!/usr/bin/env python
"""
Naver Commerce API - Deploy Service
FastAPI 部署服务接口
提供订单查询和发货状态上传功能
"""

from fastapi import FastAPI, HTTPException, Query, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import uvicorn
from datetime import datetime
import sys
import os
import subprocess
import threading
import signal
import time

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入业务逻辑函数
from deploy_code.main.setp_function_code import (
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


class UpdateDeployRequest(BaseModel):
    """代码更新请求模型"""
    secret_key: str = Field(..., description="安全密钥")
    install_dependencies: bool = Field(default=True, description="是否安装依赖包")
    restart_service: bool = Field(default=True, description="是否重启服务")


class UpdateDeployResponse(BaseModel):
    """代码更新响应模型"""
    success: bool
    git_pull_output: Optional[str] = None
    dependencies_output: Optional[str] = None
    restart_scheduled: Optional[bool] = None
    message: str
    error: Optional[str] = None


# ==================== FastAPI 应用 ====================

# 安全密钥 - 生产环境请使用环境变量
SECRET_KEY = os.environ.get("DEPLOY_SECRET_KEY", "naver_deploy_2026")

app = FastAPI(
    title="Naver Commerce Deploy API",
    description="Naver 商城部署服务 - 订单查询与发货管理",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# ==================== 辅助函数 ====================

def restart_service_delayed():
    """延迟 2 秒后重启服务"""
    time.sleep(2)
    os.kill(os.getpid(), signal.SIGTERM)


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

@app.post("/api/deploy/update", tags=["Deploy"], response_model=UpdateDeployResponse)
async def update_and_restart(request: UpdateDeployRequest):
    """
    更新代码并重启服务
    
    **功能说明:**
    - 从 Git 远程仓库拉取最新代码
    - 可选：安装/更新 Python 依赖包
    - 可选：重启服务（延迟 2 秒执行）
    
    **安全说明:**
    - 需要提供正确的 secret_key
    - 默认密钥: naver_deploy_2026
    - 生产环境请设置环境变量: DEPLOY_SECRET_KEY
    
    **请求示例:**
    ```json
    {
        "secret_key": "naver_deploy_2026",
        "install_dependencies": true,
        "restart_service": true
    }
    ```
    
    **返回:**
    - success: 是否成功
    - git_pull_output: Git pull 输出信息
    - dependencies_output: 依赖安装输出信息
    - restart_scheduled: 是否已计划重启
    - message: 操作消息
    - error: 错误信息（如果失败）
    """
    try:
        # 验证密钥
        if request.secret_key != SECRET_KEY:
            raise HTTPException(
                status_code=403,
                detail={
                    "success": False,
                    "error": "Invalid secret key",
                    "message": "密钥验证失败"
                }
            )
        
        result = {
            "success": True,
            "git_pull_output": None,
            "dependencies_output": None,
            "restart_scheduled": False,
            "message": "",
            "error": None
        }
        
        # 获取项目根目录（deploy_api.py 所在目录的上上级）
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        
        # 1. 执行 git pull
        try:
            git_process = subprocess.run(
                ["git", "pull"],
                cwd=project_root,
                capture_output=True,
                text=True,
                timeout=30
            )
            result["git_pull_output"] = git_process.stdout + git_process.stderr
            
            if git_process.returncode != 0:
                result["success"] = False
                result["error"] = f"Git pull failed: {git_process.stderr}"
                result["message"] = "代码拉取失败"
                return JSONResponse(status_code=500, content=result)
        
        except subprocess.TimeoutExpired:
            result["success"] = False
            result["error"] = "Git pull timeout"
            result["message"] = "Git 操作超时"
            return JSONResponse(status_code=500, content=result)
        
        except Exception as e:
            result["success"] = False
            result["error"] = f"Git pull error: {str(e)}"
            result["message"] = "Git 操作失败"
            return JSONResponse(status_code=500, content=result)
        
        # 2. 安装依赖包（如果需要）
        if request.install_dependencies:
            try:
                requirements_file = os.path.join(project_root, "requirements.txt")
                if os.path.exists(requirements_file):
                    pip_process = subprocess.run(
                        [sys.executable, "-m", "pip", "install", "-r", requirements_file],
                        capture_output=True,
                        text=True,
                        timeout=120
                    )
                    result["dependencies_output"] = pip_process.stdout + pip_process.stderr
                    
                    if pip_process.returncode != 0:
                        result["error"] = f"Dependency installation warning: {pip_process.stderr}"
                else:
                    result["dependencies_output"] = "requirements.txt not found, skipped"
            
            except subprocess.TimeoutExpired:
                result["error"] = "Dependency installation timeout"
            
            except Exception as e:
                result["error"] = f"Dependency installation error: {str(e)}"
        
        # 3. 计划重启服务（如果需要）
        if request.restart_service:
            # 在后台线程中延迟重启，让本次请求能够正常返回
            restart_thread = threading.Thread(target=restart_service_delayed)
            restart_thread.daemon = True
            restart_thread.start()
            result["restart_scheduled"] = True
            result["message"] = "代码更新成功，服务将在 2 秒后重启"
        else:
            result["message"] = "代码更新成功，但未重启服务"
        
        return JSONResponse(status_code=200, content=result)
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": str(e),
                "message": "服务更新失败"
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
    print("  ├─ POST /api/deploy/update      - 更新代码并重启服务")
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
