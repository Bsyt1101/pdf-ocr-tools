#!/bin/bash
# 项目打包脚本

VERSION="v1.0.0"
PROJECT_NAME="pdf-ocr-tool"
ARCHIVE_NAME="${PROJECT_NAME}-${VERSION}.tar.gz"

echo "=================================="
echo "PDF OCR 工具打包脚本"
echo "版本: ${VERSION}"
echo "=================================="

# 清理临时文件
echo "清理临时文件..."
rm -rf __pycache__
rm -f *.pyc
rm -f *.log

# 创建打包目录
echo "创建打包目录..."
TEMP_DIR="/tmp/${PROJECT_NAME}"
rm -rf ${TEMP_DIR}
mkdir -p ${TEMP_DIR}

# 复制文件
echo "复制文件..."
cp *.md ${TEMP_DIR}/
cp *.py ${TEMP_DIR}/
cp requirements.txt ${TEMP_DIR}/
cp .gitignore ${TEMP_DIR}/ 2>/dev/null || true

# 创建压缩包
echo "创建压缩包..."
cd /tmp
tar -czf ${ARCHIVE_NAME} ${PROJECT_NAME}

# 移动到当前目录
mv ${ARCHIVE_NAME} -

echo ""
echo "✓ 打包完成: ${ARCHIVE_NAME}"
echo ""
echo "分发方法:"
echo "1. 解压: tar -xzf ${ARCHIVE_NAME}"
echo "2. 进入目录: cd ${PROJECT_NAME}"
echo "3. 查看文档: cat INDEX.md"
echo ""
