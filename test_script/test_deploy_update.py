#!/usr/bin/env python
"""
测试代码更新和服务重启接口
"""

import requests
import json

# API 配置
BASE_URL = "http://localhost:8001"
SECRET_KEY = "naver_deploy_2026"  # 默认密钥，生产环境请修改


def test_update_deploy(install_deps=True, restart=True):
    """
    测试代码更新和服务重启
    
    参数:
        install_deps: 是否安装依赖包
        restart: 是否重启服务
    """
    url = f"{BASE_URL}/api/deploy/update"
    
    payload = {
        "secret_key": SECRET_KEY,
        "install_dependencies": install_deps,
        "restart_service": restart
    }
    
    print("=" * 80)
    print("📦 测试代码更新和服务重启接口")
    print("=" * 80)
    print(f"🔗 请求地址: {url}")
    print(f"📝 请求参数:")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    print("=" * 80)
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        
        print(f"📊 响应状态码: {response.status_code}")
        print("=" * 80)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 更新成功!")
            print("\n📋 详细信息:")
            print(f"  • 成功: {result.get('success')}")
            print(f"  • 消息: {result.get('message')}")
            print(f"  • 已计划重启: {result.get('restart_scheduled')}")
            
            if result.get('git_pull_output'):
                print(f"\n🔄 Git Pull 输出:")
                print("  " + "\n  ".join(result['git_pull_output'].split('\n')))
            
            if result.get('dependencies_output'):
                print(f"\n📦 依赖安装输出:")
                print("  " + "\n  ".join(result['dependencies_output'].split('\n')[:10]))  # 只显示前10行
            
            if result.get('error'):
                print(f"\n⚠️  警告: {result.get('error')}")
        
        elif response.status_code == 403:
            print("❌ 认证失败: 密钥错误")
            print(f"   响应: {response.json()}")
        
        else:
            print(f"❌ 更新失败")
            print(f"   响应: {response.json()}")
        
        print("=" * 80)
        
        return response.json()
    
    except requests.exceptions.Timeout:
        print("❌ 请求超时")
        print("=" * 80)
        return None
    
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败: 服务可能正在重启或未启动")
        print("=" * 80)
        return None
    
    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")
        print("=" * 80)
        return None


def test_service_health():
    """测试服务健康状态"""
    url = f"{BASE_URL}/health"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print("✅ 服务运行正常")
            print(f"   {response.json()}")
        else:
            print("⚠️  服务状态异常")
        return True
    except:
        print("❌ 服务未运行")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="测试代码更新和服务重启接口")
    parser.add_argument("--no-deps", action="store_true", help="不安装依赖包")
    parser.add_argument("--no-restart", action="store_true", help="不重启服务")
    parser.add_argument("--check-health", action="store_true", help="只检查服务健康状态")
    
    args = parser.parse_args()
    
    if args.check_health:
        test_service_health()
    else:
        # 测试更新
        test_update_deploy(
            install_deps=not args.no_deps,
            restart=not args.no_restart
        )
        
        # 如果选择了重启，等待几秒后检查服务状态
        if not args.no_restart:
            print("\n⏳ 等待服务重启...")
            import time
            time.sleep(5)
            print("\n🔍 检查服务状态:")
            test_service_health()
