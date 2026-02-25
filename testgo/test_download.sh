#!/bin/bash
# 测试文件下载服务的脚本

PORT=8000
BASE_URL="http://localhost:${PORT}"

echo "=========================================="
echo "文件下载服务测试脚本"
echo "=========================================="
echo ""

# 检查服务是否运行
echo "1. 检查服务是否运行..."
if curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}" | grep -q "200\|403\|404"; then
    echo "✅ 服务正在运行"
else
    echo "❌ 服务未运行，请先启动服务："
    echo "   python3 file_server.py -p ${PORT}"
    exit 1
fi
echo ""

# 测试文件列表
echo "2. 测试获取文件列表..."
curl -s "${BASE_URL}" | head -20
echo ""
echo ""

# 创建一个测试文件
TEST_FILE="test_download_$(date +%s).txt"
echo "3. 创建测试文件: ${TEST_FILE}"
echo "这是一个测试文件，用于验证下载功能" > "${TEST_FILE}"
echo "文件内容："
cat "${TEST_FILE}"
echo ""
echo ""

# 等待一下，确保文件已创建
sleep 1

# 测试下载文件
echo "4. 测试下载文件..."
DOWNLOADED_FILE="downloaded_${TEST_FILE}"
echo "正在从 ${BASE_URL}/${TEST_FILE} 下载..."
curl -o "${DOWNLOADED_FILE}" "${BASE_URL}/${TEST_FILE}"

if [ -f "${DOWNLOADED_FILE}" ]; then
    echo "✅ 文件下载成功: ${DOWNLOADED_FILE}"
    echo "文件内容："
    cat "${DOWNLOADED_FILE}"
    echo ""
    
    # 比较文件
    if cmp -s "${TEST_FILE}" "${DOWNLOADED_FILE}"; then
        echo "✅ 文件内容匹配"
    else
        echo "❌ 文件内容不匹配"
    fi
else
    echo "❌ 文件下载失败"
fi
echo ""

# 清理测试文件
echo "5. 清理测试文件..."
rm -f "${TEST_FILE}" "${DOWNLOADED_FILE}"
echo "✅ 清理完成"
echo ""

echo "=========================================="
echo "测试完成"
echo "=========================================="


