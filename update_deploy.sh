#!/bin/bash
# 代码更新和服务重启脚本
# 用法: ./update_deploy.sh [选项]

# 配置
API_URL="${API_URL:-http://localhost:8001}"
SECRET_KEY="${DEPLOY_SECRET_KEY:-naver_deploy_2026}"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 默认参数
INSTALL_DEPS=true
RESTART_SERVICE=true

# 帮助信息
show_help() {
    echo "=================================="
    echo "  代码更新和服务重启脚本"
    echo "=================================="
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -h, --help              显示此帮助信息"
    echo "  --no-deps               不安装依赖包"
    echo "  --no-restart            不重启服务"
    echo "  --check                 只检查服务状态"
    echo "  --url URL               指定 API 地址 (默认: http://localhost:8001)"
    echo "  --key KEY               指定密钥 (默认: naver_deploy_2026 或环境变量 DEPLOY_SECRET_KEY)"
    echo ""
    echo "示例:"
    echo "  $0                      # 完整更新（拉取代码 + 安装依赖 + 重启）"
    echo "  $0 --no-deps            # 只拉取代码和重启，不安装依赖"
    echo "  $0 --no-restart         # 只拉取代码和安装依赖，不重启"
    echo "  $0 --check              # 检查服务状态"
    echo ""
    echo "环境变量:"
    echo "  API_URL                 API 服务地址"
    echo "  DEPLOY_SECRET_KEY       部署密钥"
    echo ""
}

# 检查服务状态
check_service() {
    echo -e "${BLUE}🔍 检查服务状态...${NC}"
    
    response=$(curl -s -w "\n%{http_code}" "${API_URL}/health" 2>/dev/null)
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}✅ 服务运行正常${NC}"
        echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
        return 0
    else
        echo -e "${RED}❌ 服务未运行或状态异常${NC}"
        return 1
    fi
}

# 更新部署
update_deploy() {
    echo "=================================="
    echo -e "${BLUE}📦 开始更新部署${NC}"
    echo "=================================="
    echo "🔗 API 地址: ${API_URL}"
    echo "📦 安装依赖: ${INSTALL_DEPS}"
    echo "🔁 重启服务: ${RESTART_SERVICE}"
    echo "=================================="
    
    # 构建 JSON payload
    payload=$(cat <<EOF
{
  "secret_key": "${SECRET_KEY}",
  "install_dependencies": ${INSTALL_DEPS},
  "restart_service": ${RESTART_SERVICE}
}
EOF
)
    
    echo -e "${YELLOW}📤 发送更新请求...${NC}"
    
    # 发送请求
    response=$(curl -s -w "\n%{http_code}" -X POST "${API_URL}/api/deploy/update" \
        -H "Content-Type: application/json" \
        -d "$payload" \
        2>/dev/null)
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    echo "=================================="
    echo "📊 响应状态码: ${http_code}"
    echo "=================================="
    
    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}✅ 更新成功!${NC}"
        echo ""
        echo "📋 详细信息:"
        echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
        
        if [ "$RESTART_SERVICE" = "true" ]; then
            echo ""
            echo -e "${YELLOW}⏳ 服务将在 2 秒后重启，等待 5 秒后检查状态...${NC}"
            sleep 5
            echo ""
            check_service
        fi
        
        return 0
    elif [ "$http_code" = "403" ]; then
        echo -e "${RED}❌ 认证失败: 密钥错误${NC}"
        echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
        return 1
    else
        echo -e "${RED}❌ 更新失败${NC}"
        echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
        return 1
    fi
}

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        --no-deps)
            INSTALL_DEPS=false
            shift
            ;;
        --no-restart)
            RESTART_SERVICE=false
            shift
            ;;
        --check)
            check_service
            exit $?
            ;;
        --url)
            API_URL="$2"
            shift 2
            ;;
        --key)
            SECRET_KEY="$2"
            shift 2
            ;;
        *)
            echo -e "${RED}错误: 未知选项 $1${NC}"
            echo "使用 --help 查看帮助信息"
            exit 1
            ;;
    esac
done

# 执行更新
update_deploy
exit $?
